
# SpiralOS UI – Development & Runtime Guide

This guide documents the setup, build, test, and runtime procedures for the `spiralos-ui` application inside the `SpiralOS` project.

---

## ✅ Development Setup

1. **Install dependencies**

   ```bash
   npm install
   ```
2. **Start dev server**

   ```bash
   npm run dev
   ```

   > Serves on: `http://localhost:3000`
   >
3. **Lint & Format (optional)**

   ```bash
   npm run lint
   npm run format
   ```

---

## ✅ Testing Setup

We use `Jest`, `React Testing Library`, and `ts-jest` with support for JSDOM.

### Key files:

* `jest.config.js` – custom transform for `.ts`/`.tsx`, ESModules in `node_modules`, path aliases
* `jest.setup.ts` – includes `@testing-library/jest-dom`, `whatwg-fetch`, and global test setup

### Run tests

```bash
npm test
```

> ✅ All tests pass and ApolloProvider is mocked. See `__tests__/SpiralGraphUI.test.tsx` for the main suite.

### Mocking GraphQL + Apollo

* Apollo Client is wrapped inside `ApolloProvider` in tests.
* Network requests and `fetch` are polyfilled.

---

## ✅ PM2 Runtime (Production)

### 1. **Build the UI**

```bash
npm run build
```

### 2. **Start with PM2**

```bash
pm install -g pm2  # if not already installed
pm2 start ecosystem.config.js
pm2 save
```

To restart after build:

```bash
~/.npm-global/bin/pm2 restart spiralos-ui
```

> Ensure your `.npm-global/bin` is in `$PATH`, or use the full path as above.

### 3. **Access logs**

```bash
pm2 logs spiralos-ui
```

---

## 🛠 Troubleshooting

* **`pm2` not found?** Add this to your `~/.bashrc` or `~/.zshrc`:
  ```bash
  export PATH="$PATH:$HOME/.npm-global/bin"
  ```
* **Next.js build errors?** Check for:
  * `Server Actions must be async` → don't use `this` or `arguments`
  * Legacy Babel transforms from `.babelrc`

---

## 🔜 Planned Enhancements

* Snapshot testing for UI regressions
* Mock service worker integration for full GraphQL test coverage
* PM2 auto-restart on deploy

---

Carefully maintained by the SpiralOS Fellowship.
