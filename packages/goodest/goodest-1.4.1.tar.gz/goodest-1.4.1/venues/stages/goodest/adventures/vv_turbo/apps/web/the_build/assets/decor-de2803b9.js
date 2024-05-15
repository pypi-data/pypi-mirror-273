import{_ as x,r as d,o as M,f as C,w as o,a as n,g as i,h as a,m as R,q as S,u as k}from"./index-a0b775e5.js";import O from"./field-a31efeca.js";const W={},z=n("header",null,[n("h2",{style:{margin:"0 0 10px",textAlign:"center"}},"custom controls"),n("p",{style:{margin:"0 0 10px",textAlign:"center"}},"These controls are custom for this site.")],-1),N=n("h2",{style:{margin:0}},"landmarks",-1),j={style:{display:"flex",justifyContent:"space-between",padding:"3px 0"}},$={style:{display:"flex",justifyContent:"space-between",padding:"3px 0"}};function X(g,w){const l=d("hw_button"),h=d("s_paragraph"),m=d("s_panel");return M(),C(m,null,{default:o(()=>[z,n("article",null,[N,n("section",j,[i(l,null,{default:o(()=>[a("l")]),_:1}),i(h,null,{default:o(()=>[a("finds the next landmark")]),_:1})]),n("section",$,[i(h,null,{default:o(()=>[i(l,null,{default:o(()=>[a("l")]),_:1}),a(" and "),i(l,{expandable:!0},{default:o(()=>[a("shift")]),_:1})]),_:1}),i(h,null,{default:o(()=>[a("finds the previous next landmark")]),_:1})])])]),_:1})}const Y=x(W,[["render",X]]),V={},P=n("header",null,[n("h2",{style:{margin:"0 0 10px",textAlign:"center"}},"browser controls"),n("p",{style:{margin:"0 0 10px",textAlign:"center"}},"These controls are possible in most browsers.")],-1),H=n("h3",{style:{margin:0}},"moving focus",-1),L={style:{display:"flex",justifyContent:"space-between",padding:"3px 0"}},q={style:{display:"flex",justifyContent:"space-between",padding:"3px 0"}},B=n("div",{style:{height:"20px"}},null,-1),F=n("h3",{style:{margin:0}},"address navigation",-1),U={style:{display:"flex",justifyContent:"space-between",padding:"3px 0"}},G={style:{display:"flex",justifyContent:"space-between",padding:"3px 0"}},I={style:{display:"flex",justifyContent:"space-between",padding:"3px 0"}},D=n("div",{style:{height:"10px"}},null,-1),J=n("h3",{style:{margin:0}},"bookmarks",-1),K={style:{display:"flex",justifyContent:"space-between"}};function Q(g,w){const l=d("hw_button"),h=d("s_paragraph"),m=d("s_panel");return M(),C(m,null,{default:o(()=>[P,n("article",null,[H,n("section",L,[i(h,null,{default:o(()=>[i(l,{expandable:""},{default:o(()=>[a("tab")]),_:1})]),_:1}),i(h,null,{default:o(()=>[a("finds the next focusable component")]),_:1})]),n("section",q,[i(h,null,{default:o(()=>[i(l,{expandable:""},{default:o(()=>[a("tab")]),_:1}),a(" and "),i(l,{expandable:""},{default:o(()=>[a("shift")]),_:1})]),_:1}),i(h,null,{default:o(()=>[a("finds the previous focusable component")]),_:1})])]),B,n("section",null,[F,n("article",U,[i(h,null,{default:o(()=>[i(l,{expandable:""},{default:o(()=>[a("alt")]),_:1}),a(" and "),i(l,{expandable:""},{default:o(()=>[a("left arrow")]),_:1})]),_:1}),i(h,null,{default:o(()=>[a("go back")]),_:1})]),n("article",G,[i(h,null,{default:o(()=>[i(l,{expandable:""},{default:o(()=>[a("alt")]),_:1}),a(" and "),i(l,{expandable:""},{default:o(()=>[a("right arrow")]),_:1})]),_:1}),i(h,null,{default:o(()=>[a("go forward")]),_:1})]),n("article",I,[i(h,null,{default:o(()=>[i(l,{expandable:""},{default:o(()=>[a("control")]),_:1}),a(" and "),i(l,null,{default:o(()=>[a("r")]),_:1})]),_:1}),i(h,null,{default:o(()=>[a("refresh")]),_:1})])]),D,n("section",null,[J,n("article",K,[i(h,null,{default:o(()=>[i(l,{expandable:""},{default:o(()=>[a("control")]),_:1}),a(" and "),i(l,null,{default:o(()=>[a("d")]),_:1})]),_:1}),i(h,null,{default:o(()=>[a("bookmark current address")]),_:1})])])]),_:1})}const Z=x(V,[["render",Q]]),ee={},te=n("header",null,[n("h2",{style:{margin:"0 0 10px",textAlign:"center"}},"references")],-1),se=n("div",{style:{height:"10px"}},null,-1);function oe(g,w){const l=d("s_outer_link"),h=d("s_panel");return M(),C(h,null,{default:o(()=>[te,i(l,{address:"http://dmcritchie.mvps.org/firefox/keyboard.htm",style:{display:"block",padding:0}},{default:o(()=>[a(" http://dmcritchie.mvps.org/firefox/keyboard.htm ")]),_:1}),se,i(l,{address:"https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/roles/landmark_role",style:{display:"block",padding:0}},{default:o(()=>[a(" https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/roles/landmark_role ")]),_:1})]),_:1})}const ie=x(ee,[["render",oe]]);var ne={exports:{}};(function(g,w){(function(l,h){g.exports=h()})(typeof self<"u"?self:R,()=>(()=>{var l={d:(e,t)=>{for(var s in t)l.o(t,s)&&!l.o(e,s)&&Object.defineProperty(e,s,{enumerable:!0,get:t[s]})},o:(e,t)=>Object.prototype.hasOwnProperty.call(e,t),r:e=>{typeof Symbol<"u"&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}},h={};l.r(h),l.d(h,{default:()=>A}),Number.prototype.clamp=function(e,t){return Math.min(Math.max(this,e),t)};function m(e){for(;e.children&&e.children.length>0;)m(e.children[0]),e.remove(e.children[0]);e.geometry&&e.geometry.dispose(),e.material&&(Object.keys(e.material).forEach(t=>{e.material[t]&&e.material[t]!==null&&typeof e.material[t].dispose=="function"&&e.material[t].dispose()}),e.material.dispose())}const y=typeof window=="object";let f=y&&window.THREE||{};y&&!window.VANTA&&(window.VANTA={});const u=y&&window.VANTA||{};u.register=(e,t)=>u[e]=s=>new t(s),u.version="0.5.24";const v=function(){return Array.prototype.unshift.call(arguments,"[VANTA]"),console.error.apply(this,arguments)};u.VantaBase=class{constructor(e={}){if(!y)return!1;u.current=this,this.windowMouseMoveWrapper=this.windowMouseMoveWrapper.bind(this),this.windowTouchWrapper=this.windowTouchWrapper.bind(this),this.windowGyroWrapper=this.windowGyroWrapper.bind(this),this.resize=this.resize.bind(this),this.animationLoop=this.animationLoop.bind(this),this.restart=this.restart.bind(this);const t=typeof this.getDefaultOptions=="function"?this.getDefaultOptions():this.defaultOptions;if(this.options=Object.assign({mouseControls:!0,touchControls:!0,gyroControls:!1,minHeight:200,minWidth:200,scale:1,scaleMobile:1},t),(e instanceof HTMLElement||typeof e=="string")&&(e={el:e}),Object.assign(this.options,e),this.options.THREE&&(f=this.options.THREE),this.el=this.options.el,this.el==null)v('Instance needs "el" param!');else if(!(this.options.el instanceof HTMLElement)){const _=this.el;if(this.el=(s=_,document.querySelector(s)),!this.el)return void v("Cannot find element",_)}var s,r;this.prepareEl(),this.initThree(),this.setSize();try{this.init()}catch(_){return v("Init error",_),this.renderer&&this.renderer.domElement&&this.el.removeChild(this.renderer.domElement),void(this.options.backgroundColor&&(console.log("[VANTA] Falling back to backgroundColor"),this.el.style.background=(r=this.options.backgroundColor,typeof r=="number"?"#"+("00000"+r.toString(16)).slice(-6):r)))}this.initMouse(),this.resize(),this.animationLoop();const p=window.addEventListener;p("resize",this.resize),window.requestAnimationFrame(this.resize),this.options.mouseControls&&(p("scroll",this.windowMouseMoveWrapper),p("mousemove",this.windowMouseMoveWrapper)),this.options.touchControls&&(p("touchstart",this.windowTouchWrapper),p("touchmove",this.windowTouchWrapper)),this.options.gyroControls&&p("deviceorientation",this.windowGyroWrapper)}setOptions(e={}){Object.assign(this.options,e),this.triggerMouseMove()}prepareEl(){let e,t;if(typeof Node<"u"&&Node.TEXT_NODE)for(e=0;e<this.el.childNodes.length;e++){const s=this.el.childNodes[e];if(s.nodeType===Node.TEXT_NODE){const r=document.createElement("span");r.textContent=s.textContent,s.parentElement.insertBefore(r,s),s.remove()}}for(e=0;e<this.el.children.length;e++)t=this.el.children[e],getComputedStyle(t).position==="static"&&(t.style.position="relative"),getComputedStyle(t).zIndex==="auto"&&(t.style.zIndex=1);getComputedStyle(this.el).position==="static"&&(this.el.style.position="relative")}applyCanvasStyles(e,t={}){Object.assign(e.style,{position:"absolute",zIndex:0,top:0,left:0,background:""}),Object.assign(e.style,t),e.classList.add("vanta-canvas")}initThree(){f.WebGLRenderer?(this.renderer=new f.WebGLRenderer({alpha:!0,antialias:!0}),this.el.appendChild(this.renderer.domElement),this.applyCanvasStyles(this.renderer.domElement),isNaN(this.options.backgroundAlpha)&&(this.options.backgroundAlpha=1),this.scene=new f.Scene):console.warn("[VANTA] No THREE defined on window")}getCanvasElement(){return this.renderer?this.renderer.domElement:this.p5renderer?this.p5renderer.canvas:void 0}getCanvasRect(){const e=this.getCanvasElement();return!!e&&e.getBoundingClientRect()}windowMouseMoveWrapper(e){const t=this.getCanvasRect();if(!t)return!1;const s=e.clientX-t.left,r=e.clientY-t.top;s>=0&&r>=0&&s<=t.width&&r<=t.height&&(this.mouseX=s,this.mouseY=r,this.options.mouseEase||this.triggerMouseMove(s,r))}windowTouchWrapper(e){const t=this.getCanvasRect();if(!t)return!1;if(e.touches.length===1){const s=e.touches[0].clientX-t.left,r=e.touches[0].clientY-t.top;s>=0&&r>=0&&s<=t.width&&r<=t.height&&(this.mouseX=s,this.mouseY=r,this.options.mouseEase||this.triggerMouseMove(s,r))}}windowGyroWrapper(e){const t=this.getCanvasRect();if(!t)return!1;const s=Math.round(2*e.alpha)-t.left,r=Math.round(2*e.beta)-t.top;s>=0&&r>=0&&s<=t.width&&r<=t.height&&(this.mouseX=s,this.mouseY=r,this.options.mouseEase||this.triggerMouseMove(s,r))}triggerMouseMove(e,t){e===void 0&&t===void 0&&(this.options.mouseEase?(e=this.mouseEaseX,t=this.mouseEaseY):(e=this.mouseX,t=this.mouseY)),this.uniforms&&(this.uniforms.iMouse.value.x=e/this.scale,this.uniforms.iMouse.value.y=t/this.scale);const s=e/this.width,r=t/this.height;typeof this.onMouseMove=="function"&&this.onMouseMove(s,r)}setSize(){this.scale||(this.scale=1),typeof navigator<"u"&&(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)||window.innerWidth<600)&&this.options.scaleMobile?this.scale=this.options.scaleMobile:this.options.scale&&(this.scale=this.options.scale),this.width=Math.max(this.el.offsetWidth,this.options.minWidth),this.height=Math.max(this.el.offsetHeight,this.options.minHeight)}initMouse(){(!this.mouseX&&!this.mouseY||this.mouseX===this.options.minWidth/2&&this.mouseY===this.options.minHeight/2)&&(this.mouseX=this.width/2,this.mouseY=this.height/2,this.triggerMouseMove(this.mouseX,this.mouseY))}resize(){this.setSize(),this.camera&&(this.camera.aspect=this.width/this.height,typeof this.camera.updateProjectionMatrix=="function"&&this.camera.updateProjectionMatrix()),this.renderer&&(this.renderer.setSize(this.width,this.height),this.renderer.setPixelRatio(window.devicePixelRatio/this.scale)),typeof this.onResize=="function"&&this.onResize()}isOnScreen(){const e=this.el.offsetHeight,t=this.el.getBoundingClientRect(),s=window.pageYOffset||(document.documentElement||document.body.parentNode||document.body).scrollTop,r=t.top+s;return r-window.innerHeight<=s&&s<=r+e}animationLoop(){this.t||(this.t=0),this.t2||(this.t2=0);const e=performance.now();if(this.prevNow){let t=(e-this.prevNow)/16.666666666666668;t=Math.max(.2,Math.min(t,5)),this.t+=t,this.t2+=(this.options.speed||1)*t,this.uniforms&&(this.uniforms.iTime.value=.016667*this.t2)}return this.prevNow=e,this.options.mouseEase&&(this.mouseEaseX=this.mouseEaseX||this.mouseX||0,this.mouseEaseY=this.mouseEaseY||this.mouseY||0,Math.abs(this.mouseEaseX-this.mouseX)+Math.abs(this.mouseEaseY-this.mouseY)>.1&&(this.mouseEaseX+=.05*(this.mouseX-this.mouseEaseX),this.mouseEaseY+=.05*(this.mouseY-this.mouseEaseY),this.triggerMouseMove(this.mouseEaseX,this.mouseEaseY))),(this.isOnScreen()||this.options.forceAnimate)&&(typeof this.onUpdate=="function"&&this.onUpdate(),this.scene&&this.camera&&(this.renderer.render(this.scene,this.camera),this.renderer.setClearColor(this.options.backgroundColor,this.options.backgroundAlpha)),this.fps&&this.fps.update&&this.fps.update(),typeof this.afterRender=="function"&&this.afterRender()),this.req=window.requestAnimationFrame(this.animationLoop)}restart(){if(this.scene)for(;this.scene.children.length;)this.scene.remove(this.scene.children[0]);typeof this.onRestart=="function"&&this.onRestart(),this.init()}init(){typeof this.onInit=="function"&&this.onInit()}destroy(){typeof this.onDestroy=="function"&&this.onDestroy();const e=window.removeEventListener;e("touchstart",this.windowTouchWrapper),e("touchmove",this.windowTouchWrapper),e("scroll",this.windowMouseMoveWrapper),e("mousemove",this.windowMouseMoveWrapper),e("deviceorientation",this.windowGyroWrapper),e("resize",this.resize),window.cancelAnimationFrame(this.req);const t=this.scene;t&&t.children&&m(t),this.renderer&&(this.renderer.domElement&&this.el.removeChild(this.renderer.domElement),this.renderer=null,this.scene=null),u.current===this&&(u.current=null)}};const E=u.VantaBase;let c=typeof window=="object"&&window.THREE;class T extends E{constructor(t){c=t.THREE||c,c.Color.prototype.toVector=function(){return new c.Vector3(this.r,this.g,this.b)},super(t),this.updateUniforms=this.updateUniforms.bind(this)}init(){this.mode="shader",this.uniforms={iTime:{type:"f",value:1},iResolution:{type:"v2",value:new c.Vector2(1,1)},iDpr:{type:"f",value:window.devicePixelRatio||1},iMouse:{type:"v2",value:new c.Vector2(this.mouseX||0,this.mouseY||0)}},super.init(),this.fragmentShader&&this.initBasicShader()}setOptions(t){super.setOptions(t),this.updateUniforms()}initBasicShader(t=this.fragmentShader,s=this.vertexShader){s||(s=`uniform float uTime;
uniform vec2 uResolution;
void main() {
  gl_Position = vec4( position, 1.0 );
}`),this.updateUniforms(),typeof this.valuesChanger=="function"&&this.valuesChanger();const r=new c.ShaderMaterial({uniforms:this.uniforms,vertexShader:s,fragmentShader:t}),p=this.options.texturePath;p&&(this.uniforms.iTex={type:"t",value:new c.TextureLoader().load(p)});const _=new c.Mesh(new c.PlaneGeometry(2,2),r);this.scene.add(_),this.camera=new c.Camera,this.camera.position.z=1}updateUniforms(){const t={};let s,r;for(s in this.options)r=this.options[s],s.toLowerCase().indexOf("color")!==-1?t[s]={type:"v3",value:new c.Color(r).toVector()}:typeof r=="number"&&(t[s]={type:"f",value:r});return Object.assign(this.uniforms,t)}resize(){super.resize(),this.uniforms.iResolution.value.x=this.width/this.scale,this.uniforms.iResolution.value.y=this.height/this.scale}}class b extends T{}const A=u.register("FOG",b);return b.prototype.defaultOptions={highlightColor:16761600,midtoneColor:16719616,lowlightColor:2949375,baseColor:16772075,blurFactor:.6,speed:1,zoom:1,scale:2,scaleMobile:4},b.prototype.fragmentShader=`uniform vec2 iResolution;
uniform vec2 iMouse;
uniform float iTime;

uniform float blurFactor;
uniform vec3 baseColor;
uniform vec3 lowlightColor;
uniform vec3 midtoneColor;
uniform vec3 highlightColor;
uniform float zoom;

float random (in vec2 _st) {
  return fract(sin(dot(_st.xy,
                     vec2(0.129898,0.78233)))*
        437.585453123);
}

// Based on Morgan McGuire @morgan3d
// https://www.shadertoy.com/view/4dS3Wd
float noise (in vec2 _st) {
  vec2 i = floor(_st);
  vec2 f = fract(_st);

  // Four corners in 2D of a tile
  float a = random(i);
  float b = random(i + vec2(1.0, 0.0));
  float c = random(i + vec2(0.0, 1.0));
  float d = random(i + vec2(1.0, 1.0));

  vec2 u = f * f * (3.0 - 2.0 * f);

  return mix(a, b, u.x) +
          (c - a)* u.y * (1.0 - u.x) +
          (d - b) * u.x * u.y;
}

#define NUM_OCTAVES 6

float fbm ( in vec2 _st) {
  float v = 0.0;
  float a = blurFactor;
  vec2 shift = vec2(100.0);
  // Rotate to reduce axial bias
  mat2 rot = mat2(cos(0.5), sin(0.5),
                  -sin(0.5), cos(0.50));
  for (int i = 0; i < NUM_OCTAVES; ++i) {
      v += a * noise(_st);
      _st = rot * _st * 2.0 + shift;
      a *= (1. - blurFactor);
  }
  return v;
}

void main() {
  vec2 st = gl_FragCoord.xy / iResolution.xy*3.;
  st.x *= 0.7 * iResolution.x / iResolution.y ; // Still keep it more landscape than square
  st *= zoom;

  // st += st * abs(sin(iTime*0.1)*3.0);
  vec3 color = vec3(0.0);

  vec2 q = vec2(0.);
  q.x = fbm( st + 0.00*iTime);
  q.y = fbm( st + vec2(1.0));

  vec2 dir = vec2(0.15,0.126);
  vec2 r = vec2(0.);
  r.x = fbm( st + 1.0*q + vec2(1.7,9.2)+ dir.x*iTime );
  r.y = fbm( st + 1.0*q + vec2(8.3,2.8)+ dir.y*iTime);

  float f = fbm(st+r);

  color = mix(baseColor,
              lowlightColor,
              clamp((f*f)*4.0,0.0,1.0));

  color = mix(color,
              midtoneColor,
              clamp(length(q),0.0,1.0));

  color = mix(color,
              highlightColor,
              clamp(length(r.x),0.0,1.0));

  vec3 finalColor = mix(baseColor, color, f*f*f+.6*f*f+.5*f);
  gl_FragColor = vec4(finalColor,1.0);
}
`,h})())})(ne);const re={components:{physics:O,panel_scenery:S,hw_button:k,custom_physics:Y,generic_physics:Z,references:ie},methods:{},props:{},data(){return{}},created(){},beforeMount(){},mounted(){},beforeUnmount(){},beforeDestroy(){}},ae=re,le={ref:"foundation",style:{width:"100%",borderRadius:"12px",overflow:"hidden"}},he={style:{padding:".2in",maxWidth:"1000px",margin:"0 auto"}},ce=n("div",{style:{height:"20px"}},null,-1),de=n("div",{style:{height:"20px"}},null,-1),ue=n("header",null,[n("h2",{style:{margin:"0 0 10px",textAlign:"center"}},"content options")],-1),pe=n("div",{style:{height:"20px"}},null,-1),me=n("div",{style:{height:"20px"}},null,-1);function fe(g,w,l,h,m,y){const f=d("custom_physics"),u=d("physics"),v=d("s_panel"),E=d("generic_physics"),c=d("lounge");return M(),C(c,null,{default:o(({palette:T,terrain:b})=>[n("div",le,[n("div",he,[ce,i(f,{style:{padding:".25in"}}),de,i(v,null,{default:o(()=>[ue,i(u)]),_:1}),pe,i(E,{style:{padding:".25in"}}),me])],512)]),_:1})}const ye=x(ae,[["render",fe]]);export{ye as default};
