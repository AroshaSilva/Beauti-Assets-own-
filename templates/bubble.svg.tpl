<svg xmlns="http://www.w3.org/2000/svg" width="{{WIDTH}}" height="{{HEIGHT}}" viewBox="0 0 {{WIDTH}} {{HEIGHT}}">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{{FROM}}"/>
      <stop offset="100%" stop-color="{{TO}}"/>
    </linearGradient>
  </defs>
  <path d="M20 10 H{{INNER_W}} Q{{RIGHT}} 10 {{RIGHT}} 20 V70 Q{{RIGHT}} 80 {{INNER_W}} 80 H60 L35 95 L40 80 H20 Q10 80 10 70 V20 Q10 10 20 10 Z" fill="url(#g)"/>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
        font-family="Segoe UI, Arial, sans-serif" font-size="{{FONT_SIZE}}" font-weight="600" fill="{{FONT_COLOR}}">
    {{TEXT}}
  </text>
</svg>
