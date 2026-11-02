<svg xmlns="http://www.w3.org/2000/svg" width="{{WIDTH}}" height="{{HEIGHT}}" viewBox="0 0 {{WIDTH}} {{HEIGHT}}">
  <defs>
    <linearGradient id="grad1" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{{FROM}}"/>
      <stop offset="1" stop-color="{{TO}}"/>
    </linearGradient>
  </defs>
  <rect x="10" y="10" width="{{INNER_W}}" height="70" rx="10" ry="10" fill="url(#grad1)"/>
  <path d="M60 80 L35 95 L40 80 Z" fill="{{TO}}"/>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
        font-family="Segoe UI, Arial, sans-serif" font-size="{{FONT_SIZE}}" font-weight="600" fill="{{FONT_COLOR}}">
    {{TEXT}}
  </text>
</svg>
