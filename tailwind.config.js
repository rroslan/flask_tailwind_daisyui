module.exports = {
  content: [
    "./app/templates/**/*.{html,js}",
    "./app/blueprints/**/templates/**/*.html",
    "./app/static/src/**/*.js",
    "./app/**/*.html"
  ],
  theme: {
    extend: {},
  },
  safelist: [
    'alert-{success,warning,error,info}',
    'btn-{primary,secondary,accent,ghost}',
    {
      pattern: /(bg|text|border|ring)-(red|blue|green|yellow|indigo|purple|pink|gray)-(100|200|300|400|500|600|700|800|900)/
    }
  ],
  plugins: [
    require("daisyui")
  ],
  daisyui: {
    themes: [
      {
        light: {
          "primary": "#570df8",
          "secondary": "#f000b8",
          "accent": "#1dcdbc",
          "neutral": "#2b3440",
          "base-100": "#ffffff",
          "info": "#3abff8",
          "success": "#36d399",
          "warning": "#fbbd23",
          "error": "#f87272",
        }
      }
    ],
    base: true,
    utils: true,
    logs: true,
    rtl: false,
    prefix: "",
    darkTheme: "dark",
  },
}

