module.exports = {
  apps: [
    {
      name: 'spiralos-ui',
      cwd: '/home/carey/Development/contributions/SpiralOS',
      script: 'node_modules/next/dist/bin/next',
      args: 'start',
      env: {
        NODE_ENV: 'production',
        PORT: 3000, // or whatever port you wish
      },
    },
  ],
}
