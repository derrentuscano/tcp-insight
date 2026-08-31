"""Reusable educational interface components for TCP Insight Lab."""

import streamlit.components.v1 as components


def handshake_animation() -> None:
    """Display a self-contained looping CSS animation of TCP connection setup."""
    components.html("""
    <style>
      * { box-sizing: border-box; } body { margin: 0; font-family: Inter, -apple-system, sans-serif; color: #12233f; }
      .stage { background: linear-gradient(135deg,#f8fbff,#eef6ff); border:1px solid #d7e6fb; border-radius:18px; padding:30px 34px 22px; min-height:292px; overflow:hidden; }
      .people { display:flex; justify-content:space-between; align-items:center; position:relative; margin-top:36px; }
      .node { z-index:3; width:132px; text-align:center; } .icon { width:64px; height:64px; margin:0 auto 9px; border-radius:18px; display:grid; place-items:center; font-size:30px; background:#fff; box-shadow:0 8px 18px #94b8e035; }
      .client .icon{border:2px solid #1e64e8}.server .icon{border:2px solid #0f9f75}.role{font-weight:750;font-size:15px}.sub{color:#63738a;font-size:12px;margin-top:3px}
      .rail{position:absolute;height:4px;left:118px;right:118px;top:31px;background:#c9d9ed;border-radius:4px}.packet{opacity:0;position:absolute;top:-13px;z-index:2;padding:6px 10px;border-radius:20px;color:#fff;font-size:12px;font-weight:750;box-shadow:0 6px 12px #31578035}
      .syn{background:#1e64e8;animation:right 9s infinite}.synack{background:#0f9f75;animation:left 9s infinite}.ack{background:#7a4ee4;animation:right2 9s infinite}
      @keyframes right{0%,3%{opacity:0;left:15%}5%,25%{opacity:1}28%,100%{opacity:0;left:77%}}@keyframes left{0%,32%{opacity:0;left:77%}35%,55%{opacity:1}59%,100%{opacity:0;left:15%}}@keyframes right2{0%,63%{opacity:0;left:15%}66%,87%{opacity:1}91%,100%{opacity:0;left:77%}}
      .legend{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:36px}.item{background:#fff;border:1px solid #dfebf8;border-radius:10px;padding:9px 11px;font-size:12px}.num{display:inline-grid;place-items:center;width:18px;height:18px;margin-right:5px;border-radius:50%;background:#e9f2ff;color:#1e64e8;font-weight:800}
    </style><div class="stage"><div class="people"><div class="rail"></div><div class="packet syn">SYN →</div><div class="packet synack">← SYN + ACK</div><div class="packet ack">ACK →</div><div class="node client"><div class="icon">💻</div><div class="role">Client</div><div class="sub">Initiates the connection</div></div><div class="node server"><div class="icon">🖥️</div><div class="role">Server</div><div class="sub">Accepts the connection</div></div></div><div class="legend"><div class="item"><span class="num">1</span><b>SYN</b> — client requests a connection.</div><div class="item"><span class="num">2</span><b>SYN-ACK</b> — server accepts and acknowledges.</div><div class="item"><span class="num">3</span><b>ACK</b> — client confirms; data transfer begins.</div></div></div>
    """, height=300, scrolling=False)
