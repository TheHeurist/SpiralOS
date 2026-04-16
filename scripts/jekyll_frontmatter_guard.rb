#!/usr/bin/env ruby
# frozen_string_literal: true

require 'optparse'
require 'pathname'
require 'psych'

# (Paste the full script content here)
set -euo pipefail

mkdir -p scripts

cat > scripts/jekyll_frontmatter_guard.rb <<'RUBY'
#!/usr/bin/env ruby
# frozen_string_literal: true

require 'optparse'
require 'pathname'
require 'psych'

options = {
  root: 'docs',
  autofix: false,
  verbose: false
}

OptionParser.new do |opts|
  opts.banner = 'Usage: jekyll_frontmatter_guard.rb [options] [files ...]'

  opts.on('--root PATH', 'Directory to scan when no files are provided (default: docs)') do |path|
    options[:root] = path
  end

  opts.on('--autofix', 'Auto-fix missing closing front matter delimiters when safe') do
    options[:autofix] = true
  end

  opts.on('-v', '--verbose', 'Print pass details') do
    options[:verbose] = true
  end
end.parse!

files = ARGV

if files.empty?
  root = Pathname.new(options[:root])
  files = Dir.glob(root.join('**', '*').to_s).select { |p| File.file?(p) }
end

FRONT_MATTER_START = /\A---\s*\r?\n/
FRONT_MATTER_DELIMITER = /\A(?:---|\.\.\.)\s*\z/

Issue = Struct.new(:file, :line, :message, keyword_init: true)
issues = []
fixed = []

def quote_if_needed(value)
  stripped = value.strip
  return stripped if stripped.start_with?('"', "'", '[', '{')
  return stripped unless stripped.include?(': ')

  '"' + stripped.gsub('"', '\"') + '"'
end

def normalize_front_matter(front_matter)
  lines = front_matter.lines
  normalized = []
  list_key_open = false
  block_scalar_open = false

  lines.each do |line|
    raw = line.chomp
    stripped = raw.strip

    if block_scalar_open
      if stripped.match?(/\A[A-Za-z0-9_-]+:\s*.*\z/) && !raw.start_with?(' ')
        block_scalar_open = false
      else
        normalized << (raw.start_with?(' ') || stripped.empty? ? "#{raw}\n" : "  #{raw}\n")
        next
      end
    end

    if stripped.empty?
      normalized << line
      next
    end

    if stripped.match?(/\A[A-Za-z0-9_-]+:\s*[>|]-?\s*\z/)
      block_scalar_open = true
      list_key_open = false
      normalized << "#{raw}\n"
      next
    end

    if stripped.match?(/\A[A-Za-z0-9_-]+:\s*\z/)
      list_key_open = true
      normalized << "#{raw}\n"
      next
    end

    if stripped.start_with?('* ')
      value = stripped[2..]
      if list_key_open
        normalized << "  - #{quote_if_needed(value)}\n"
      else
        normalized << "- #{quote_if_needed(value)}\n"
      end
      next
    end

    if stripped.start_with?('- ')
      indent = line[/\A\s*/] || ''
      value = stripped[2..]
      normalized << "#{indent}- #{quote_if_needed(value)}\n"
      next
    end

    list_key_open = false
    normalized << "#{raw}\n"
  end

  normalized.join
end

files.each do |file|
  begin
    raw = File.binread(file)
    text = raw.dup.force_encoding('UTF-8')
    text = text.encode('UTF-8', invalid: :replace, undef: :replace, replace: '�') unless text.valid_encoding?
  rescue StandardError
    next
  end

  next unless FRONT_MATTER_START.match?(text)

  lines = text.lines
  closing_index = nil
  lines.each_with_index do |line, idx|
    next if idx.zero?
    if FRONT_MATTER_DELIMITER.match?(line.strip)
      closing_index = idx
      break
    end
  end

  if closing_index.nil?
    if options[:autofix]
      insertion = nil
      lines.each_with_index do |line, idx|
        next if idx.zero?
        if line.strip.empty?
          insertion = idx
          break
        end
      end

      if insertion
        lines.insert(insertion, "---\n")
        File.write(file, lines.join)
        fixed << file
        next
      end
    end

    issues << Issue.new(file: file, line: 1, message: 'missing closing front matter delimiter')
    next
  end

  front_matter = lines[1...closing_index].join
  front_matter_start_line = 2

  begin
    Psych.parse(front_matter)
    puts "PASS #{file}" if options[:verbose]
  rescue Psych::SyntaxError => e
    if options[:autofix]
      normalized = normalize_front_matter(front_matter)
      if normalized != front_matter
        begin
          Psych.parse(normalized)
          rebuilt = [lines[0], normalized, lines[closing_index..].join].join
          File.write(file, rebuilt)
          fixed << file
          next
        rescue Psych::SyntaxError
        end
      end
    end

    line = e.message[/line (\d+)/, 1]
    line = line ? line.to_i + front_matter_start_line : 1
    issues << Issue.new(file: file, line: line, message: e.message.lines.first.strip)
  end
end

fixed.each { |file| puts "FIXED #{file}" }

if issues.any?
  issues.each { |issue| warn "FAIL #{issue.file}:#{issue.line} #{issue.message}" }
  exit 1
end

puts "OK: checked #{files.size} file(s); fixed #{fixed.size} file(s)."
RUBY

cat > scripts/prepush_docs_checks.sh <<'BASH'
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

warn_missing=0

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

run_or_warn() {
  local label="$1"
  local binary="$2"
  if command_exists "$binary"; then
    echo "[ok] ${label} available"
    return 0
  fi
  echo "[warn] ${label} not installed/available; skipping"
  warn_missing=$((warn_missing + 1))
  return 1
}

echo "== SpiralOS docs pre-push checks =="

if run_or_warn "yamllint" "yamllint"; then
  echo "-> yamllint docs/"
  yamllint docs/
fi

if run_or_warn "markdownlint-cli" "markdownlint"; then
  echo "-> markdownlint docs/**/*.md"
  mapfile -d '' markdown_files < <(find docs -type f -name '*.md' -print0)
  if [[ ${#markdown_files[@]} -gt 0 ]]; then
    markdownlint "${markdown_files[@]}"
  fi
fi

if run_or_warn "pre-commit" "pre-commit"; then
  echo "-> pre-commit run --all-files"
  pre-commit run --all-files
fi

echo "-> ruby front matter guard"
ruby scripts/jekyll_frontmatter_guard.rb --root docs

if run_or_warn "bundle" "bundle"; then
  if [[ -f Gemfile ]]; then
    echo "-> bundle exec jekyll build"
    bundle exec jekyll build
  else
    echo "[warn] Gemfile not found; skipping bundle exec jekyll build"
    warn_missing=$((warn_missing + 1))
  fi
fi

if run_or_warn "htmlproofer" "htmlproofer"; then
  if [[ -d _site ]]; then
    echo "-> htmlproofer _site --only-4xx --check-html"
    htmlproofer _site --only-4xx --check-html
  else
    echo "[warn] _site does not exist; run jekyll build first"
    warn_missing=$((warn_missing + 1))
  fi
fi

if [[ $warn_missing -gt 0 ]]; then
  echo "Completed with ${warn_missing} warning(s) for missing tools/prereqs."
else
  echo "All configured checks completed successfully."
fi
BASH

cat > scripts/test_jekyll_frontmatter_guard.rb <<'RUBY'
#!/usr/bin/env ruby
# frozen_string_literal: true

require 'fileutils'
require 'minitest/autorun'
require 'open3'
require 'tmpdir'

class JekyllFrontmatterGuardTest < Minitest::Test
  def setup
    @tmp = Dir.mktmpdir('jekyll-frontmatter-guard-test-')
    @script = File.expand_path('jekyll_frontmatter_guard.rb', __dir__)
  end

  def teardown
    FileUtils.remove_entry(@tmp)
  end

  def run_guard(*args)
    Open3.capture3('ruby', @script, *args, chdir: @tmp)
  end

  def write(path, content)
    full = File.join(@tmp, path)
    FileUtils.mkdir_p(File.dirname(full))
    File.write(full, content)
  end

  def test_passes_valid_front_matter
    write('docs/good.md', "---\ntitle: ok\n---\n\nBody\n")
    out, err, status = run_guard('--root', 'docs')
    assert status.success?, "Expected success, got stderr: #{err}"
    assert_includes out, 'OK: checked 1 file(s); fixed 0 file(s).'
  end

  def test_reports_missing_closing_delimiter
    write('docs/bad.md', "---\ntitle: broken\n\nBody\n")
    out, err, status = run_guard('--root', 'docs')
    refute status.success?
    assert_empty out
    assert_includes err, 'missing closing front matter delimiter'
  end

  def test_autofix_inserts_missing_delimiter
    target = 'docs/autofix.md'
    write(target, "---\ntitle: fixed\n\nBody\n")
    out, err, status = run_guard('--root', 'docs', '--autofix')
    assert status.success?, "Expected success, got stderr: #{err}"
    assert_includes out, 'FIXED docs/autofix.md'
    content = File.read(File.join(@tmp, target))
    assert_includes content, "---\ntitle: fixed\n---\n\nBody\n"
  end

  def test_parses_file_with_front_matter_and_markdown_rule
    write('docs/rule.md', "---\ntitle: ok\n---\n\nIntro\n\n---\n\nAfter rule\n")
    out, err, status = run_guard('--root', 'docs')
    assert status.success?, "Expected success, got stderr: #{err}"
    assert_includes out, 'OK: checked 1 file(s); fixed 0 file(s).'
  end

  def test_autofix_normalizes_star_lists_and_colon_scalars
    target = 'docs/lists.md'
    write(target, "---\nsection:\n* name: value\n* plain\n---\n\nBody\n")
    out, err, status = run_guard('--root', 'docs', '--autofix')
    assert status.success?, "Expected success, got stderr: #{err}"
    assert_includes out, 'FIXED docs/lists.md'
    content = File.read(File.join(@tmp, target))
    assert_includes content, "section:\n  - \"name: value\"\n  - plain\n"
  end

  def test_autofix_indents_block_scalar_contents
    target = 'docs/scalar.md'
    write(target, "---\nsummary: >\nnot indented text\nnext_key: ok\n---\n\nBody\n")
    out, err, status = run_guard('--root', 'docs', '--autofix')
    assert status.success?, "Expected success, got stderr: #{err}"
    assert_includes out, 'FIXED docs/scalar.md'
    content = File.read(File.join(@tmp, target))
    assert_includes content, "summary: >\n  not indented text\nnext_key: ok\n"
  end
end
RUBY

chmod +x scripts/jekyll_frontmatter_guard.rb scripts/prepush_docs_checks.sh scripts/test_jekyll_frontmatter_guard.rb

python3 - <<'PY'
from pathlib import Path

pc = Path(".pre-commit-config.yaml")
if pc.exists():
    t = pc.read_text(encoding="utf-8")
    if "jekyll-frontmatter-guard" not in t:
        t += """

  - repo: local
    hooks:
      - id: jekyll-frontmatter-guard
        name: jekyll-frontmatter-guard
        entry: ruby scripts/jekyll_frontmatter_guard.rb
        language: system
        files: ^docs/.*\\.(md|markdown|html)$
"""
        pc.write_text(t, encoding="utf-8")

rd = Path("README.md")
if rd.exists():
    t = rd.read_text(encoding="utf-8")
    marker = "## Docs quality gates (local)"
    if marker not in t:
        t += """

## Docs quality gates (local)

- Front matter validation: `ruby scripts/jekyll_frontmatter_guard.rb --root docs`
- Full local pre-push checks: `bash scripts/prepush_docs_checks.sh`
- Guard self-test suite: `ruby scripts/test_jekyll_frontmatter_guard.rb`

These checks are designed to catch Jekyll/front matter issues before CI.
"""
        rd.write_text(t, encoding="utf-8")
PY

ruby scripts/jekyll_frontmatter_guard.rb --root docs --autofix
ruby scripts/jekyll_frontmatter_guard.rb --root docs
ruby scripts/test_jekyll_frontmatter_guard.rb

git add .pre-commit-config.yaml README.md scripts docs
git commit -m "Add Jekyll frontmatter guard, pre-push docs checks, and normalize docs front matter"

echo
echo "Done. Now publish:"
echo "  git push -u origin work"
echo "Then open PR: work -> main"
