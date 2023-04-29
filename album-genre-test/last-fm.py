#Imports
from bs4 import BeautifulSoup
import requests , re , random , os ,time,sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import logging
from unidecode import unidecode
from proxy_checker import *

"""
lastfm.py
"""


"""
Process:

I have 1420 songs 

i got 1075 items back from genre search

1) update my lyric data with the genre 

2) find the songs that didnt get a genre

3) try this process again with only those songs  

"""

def test_site_string():
    return  """<!DOCTYPE html>

<html class="no-js playbar-masthead-release-shim youtube-provider-not-ready" lang="en">
<head>
<meta charset="utf-8"/>
<meta content="IE=edge" http-equiv="X-UA-Compatible"/><script type="text/javascript">(window.NREUM||(NREUM={})).init={ajax:{deny_list:["bam.nr-data.net"]}};(window.NREUM||(NREUM={})).loader_config={xpid:"UwYPV15QGwYFXFlXDgU=",licenseKey:"0ed0ce50b0",applicationID:"5588594"};;(()=>{var e,t,r={9071:(e,t,r)=>{"use strict";r.d(t,{I:()=>n});var n=0,i=navigator.userAgent.match(/Firefox[\/\s](\d+\.\d+)/);i&&(n=+i[1])},6562:(e,t,r)=>{"use strict";r.d(t,{P_:()=>p,Mt:()=>v,C5:()=>d,DL:()=>y,OP:()=>k,lF:()=>H,Yu:()=>E,Dg:()=>g,CX:()=>f,GE:()=>w,sU:()=>L});var n={};r.r(n),r.d(n,{agent:()=>x,match:()=>_,version:()=>O});var i=r(6797),o=r(909),a=r(8610);class s{constructor(e,t){try{if(!e||"object"!=typeof e)return(0,a.Z)("New setting a Configurable requires an object as input");if(!t||"object"!=typeof t)return(0,a.Z)("Setting a Configurable requires a model to set its initial properties");Object.assign(this,t),Object.entries(e).forEach((e=>{let[t,r]=e;const n=(0,o.q)(t);n.length&&r&&"object"==typeof r&&n.forEach((e=>{e in r&&((0,a.Z)('"'.concat(e,'" is a protected attribute and can not be changed in feature ').concat(t,".  It will have no effect.")),delete r[e])})),this[t]=r}))}catch(e){(0,a.Z)("An error occured while setting a Configurable",e)}}}const c={beacon:i.ce.beacon,errorBeacon:i.ce.errorBeacon,licenseKey:void 0,applicationID:void 0,sa:void 0,queueTime:void 0,applicationTime:void 0,ttGuid:void 0,user:void 0,account:void 0,product:void 0,extra:void 0,jsAttributes:{},userAttributes:void 0,atts:void 0,transactionName:void 0,tNamePlain:void 0},u={};function d(e){if(!e)throw new Error("All info objects require an agent identifier!");if(!u[e])throw new Error("Info for ".concat(e," was never set"));return u[e]}function f(e,t){if(!e)throw new Error("All info objects require an agent identifier!");u[e]=new s(t,c),(0,i.Qy)(e,u[e],"info")}const l={allow_bfcache:!1,privacy:{cookies_enabled:!0},ajax:{deny_list:void 0,enabled:!0,harvestTimeSeconds:10},distributed_tracing:{enabled:void 0,exclude_newrelic_header:void 0,cors_use_newrelic_header:void 0,cors_use_tracecontext_headers:void 0,allowed_origins:void 0},ssl:void 0,obfuscate:void 0,jserrors:{enabled:!0,harvestTimeSeconds:10},metrics:{enabled:!0,harvestTimeSeconds:10},page_action:{enabled:!0,harvestTimeSeconds:30},page_view_event:{enabled:!0},page_view_timing:{enabled:!0,harvestTimeSeconds:30},session_trace:{enabled:!0,harvestTimeSeconds:10},spa:{enabled:!0,harvestTimeSeconds:10}},h={};function p(e){if(!e)throw new Error("All configuration objects require an agent identifier!");if(!h[e])throw new Error("Configuration for ".concat(e," was never set"));return h[e]}function g(e,t){if(!e)throw new Error("All configuration objects require an agent identifier!");h[e]=new s(t,l),(0,i.Qy)(e,h[e],"config")}function v(e,t){if(!e)throw new Error("All configuration objects require an agent identifier!");var r=p(e);if(r){for(var n=t.split("."),i=0;i<n.length-1;i++)if("object"!=typeof(r=r[n[i]]))return;r=r[n[n.length-1]]}return r}const m={accountID:void 0,trustKey:void 0,agentID:void 0,licenseKey:void 0,applicationID:void 0,xpid:void 0},b={};function y(e){if(!e)throw new Error("All loader-config objects require an agent identifier!");if(!b[e])throw new Error("LoaderConfig for ".concat(e," was never set"));return b[e]}function w(e,t){if(!e)throw new Error("All loader-config objects require an agent identifier!");b[e]=new s(t,m),(0,i.Qy)(e,b[e],"loader_config")}const E=(0,i.mF)().o;var A=r(2053),x=null,O=null;if(navigator.userAgent){var T=navigator.userAgent,S=T.match(/Version\/(\S+)\s+Safari/);S&&-1===T.indexOf("Chrome")&&-1===T.indexOf("Chromium")&&(x="Safari",O=S[1])}function _(e,t){if(!x)return!1;if(e!==x)return!1;if(!t)return!0;if(!O)return!1;for(var r=O.split("."),n=t.split("."),i=0;i<n.length;i++)if(n[i]!==r[i])return!1;return!0}var I=r(5526),P=r(2374);const j="NRBA_SESSION_ID";function R(){if(!P.il)return null;try{let e;return null===(e=window.sessionStorage.getItem(j))&&(e=(0,I.ky)(16),window.sessionStorage.setItem(j,e)),e}catch(e){return null}}var D=r(8226);const C=e=>({customTransaction:void 0,disabled:!1,isolatedBacklog:!1,loaderType:void 0,maxBytes:3e4,offset:(0,A.yf)(),onerror:void 0,origin:""+P._A.location,ptid:void 0,releaseIds:{},sessionId:1==v(e,"privacy.cookies_enabled")?R():null,xhrWrappable:"function"==typeof P._A.XMLHttpRequest?.prototype?.addEventListener,userAgent:n,version:D.q}),N={};function k(e){if(!e)throw new Error("All runtime objects require an agent identifier!");if(!N[e])throw new Error("Runtime for ".concat(e," was never set"));return N[e]}function L(e,t){if(!e)throw new Error("All runtime objects require an agent identifier!");N[e]=new s(t,C(e)),(0,i.Qy)(e,N[e],"runtime")}function H(e){return function(e){try{const t=d(e);return!!t.licenseKey&&!!t.errorBeacon&&!!t.applicationID}catch(e){return!1}}(e)}},8226:(e,t,r)=>{"use strict";r.d(t,{q:()=>n});const n="1225.PROD"},9557:(e,t,r)=>{"use strict";r.d(t,{w:()=>o});var n=r(8610);const i={agentIdentifier:""};class o{constructor(e){try{if("object"!=typeof e)return(0,n.Z)("shared context requires an object as input");this.sharedContext={},Object.assign(this.sharedContext,i),Object.entries(e).forEach((e=>{let[t,r]=e;Object.keys(i).includes(t)&&(this.sharedContext[t]=r)}))}catch(e){(0,n.Z)("An error occured while setting SharedContext",e)}}}},4329:(e,t,r)=>{"use strict";r.d(t,{L:()=>d,R:()=>c});var n=r(3752),i=r(7022),o=r(4045),a=r(2325);const s={};function c(e,t){const r={staged:!1,priority:a.p[t]||0};u(e),s[e].get(t)||s[e].set(t,r)}function u(e){e&&(s[e]||(s[e]=new Map))}function d(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"",t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"feature";if(u(e),!e||!s[e].get(t))return a(t);s[e].get(t).staged=!0;const r=Array.from(s[e]);function a(t){const r=e?n.ee.get(e):n.ee,a=o.X.handlers;if(r.backlog&&a){var s=r.backlog[t],c=a[t];if(c){for(var u=0;s&&u<s.length;++u)f(s[u],c);(0,i.D)(c,(function(e,t){(0,i.D)(t,(function(t,r){r[0].on(e,r[1])}))}))}delete a[t],r.backlog[t]=null,r.emit("drain-"+t,[])}}r.every((e=>{let[t,r]=e;return r.staged}))&&(r.sort(((e,t)=>e[1].priority-t[1].priority)),r.forEach((e=>{let[t]=e;a(t)})))}function f(e,t){var r=e[1];(0,i.D)(t[r],(function(t,r){var n=e[0];if(r[0]===n){var i=r[1],o=e[3],a=e[2];i.apply(o,a)}}))}},3752:(e,t,r)=>{"use strict";r.d(t,{c:()=>f,ee:()=>u});var n=r(6797),i=r(3916),o=r(7022),a=r(6562),s="nr@context";let c=(0,n.fP)();var u;function d(){}function f(e){return(0,i.X)(e,s,l)}function l(){return new d}function h(){(u.backlog.api||u.backlog.feature)&&(u.aborted=!0,u.backlog={})}c.ee?u=c.ee:(u=function e(t,r){var n={},c={},f={},p=!1;try{p=16===r.length&&(0,a.OP)(r).isolatedBacklog}catch(e){}var g={on:b,addEventListener:b,removeEventListener:y,emit:m,get:E,listeners:w,context:v,buffer:A,abort:h,aborted:!1,isBuffering:x,debugId:r,backlog:p?{}:t&&"object"==typeof t.backlog?t.backlog:{}};return g;function v(e){return e&&e instanceof d?e:e?(0,i.X)(e,s,l):l()}function m(e,r,n,i,o){if(!1!==o&&(o=!0),!u.aborted||i){t&&o&&t.emit(e,r,n);for(var a=v(n),s=w(e),d=s.length,f=0;f<d;f++)s[f].apply(a,r);var l=O()[c[e]];return l&&l.push([g,e,r,a]),a}}function b(e,t){n[e]=w(e).concat(t)}function y(e,t){var r=n[e];if(r)for(var i=0;i<r.length;i++)r[i]===t&&r.splice(i,1)}function w(e){return n[e]||[]}function E(t){return f[t]=f[t]||e(g,t)}function A(e,t){var r=O();g.aborted||(0,o.D)(e,(function(e,n){t=t||"feature",c[n]=t,t in r||(r[t]=[])}))}function x(e){return!!O()[c[e]]}function O(){return g.backlog}}(void 0,"globalEE"),c.ee=u)},9252:(e,t,r)=>{"use strict";r.d(t,{E:()=>n,p:()=>i});var n=r(3752).ee.get("handle");function i(e,t,r,i,o){o?(o.buffer([e],i),o.emit(e,t,r)):(n.buffer([e],i),n.emit(e,t,r))}},4045:(e,t,r)=>{"use strict";r.d(t,{X:()=>o});var n=r(9252);o.on=a;var i=o.handlers={};function o(e,t,r,o){a(o||n.E,i,e,t,r)}function a(e,t,r,i,o){o||(o="feature"),e||(e=n.E);var a=t[o]=t[o]||{};(a[r]=a[r]||[]).push([e,i])}},8544:(e,t,r)=>{"use strict";r.d(t,{bP:()=>s,iz:()=>c,m$:()=>a});var n=r(2374);let i=!1,o=!1;try{const e={get passive(){return i=!0,!1},get signal(){return o=!0,!1}};n._A.addEventListener("test",null,e),n._A.removeEventListener("test",null,e)}catch(e){}function a(e,t){return i||o?{capture:!!e,passive:i,signal:t}:!!e}function s(e,t){let r=arguments.length>2&&void 0!==arguments[2]&&arguments[2];window.addEventListener(e,t,a(r))}function c(e,t){let r=arguments.length>2&&void 0!==arguments[2]&&arguments[2];document.addEventListener(e,t,a(r))}},5526:(e,t,r)=>{"use strict";r.d(t,{Ht:()=>a,M:()=>o,Rl:()=>i,ky:()=>s});var n=r(2374);function i(){var e=null,t=0,r=n._A?.crypto||n._A?.msCrypto;function i(){return e?15&e[t++]:16*Math.random()|0}r&&r.getRandomValues&&(e=r.getRandomValues(new Uint8Array(31)));for(var o,a="xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx",s="",c=0;c<a.length;c++)s+="x"===(o=a[c])?i().toString(16):"y"===o?(o=3&i()|8).toString(16):o;return s}function o(){return s(16)}function a(){return s(32)}function s(e){var t=null,r=0,n=self.crypto||self.msCrypto;n&&n.getRandomValues&&Uint8Array&&(t=n.getRandomValues(new Uint8Array(31)));for(var i=[],o=0;o<e;o++)i.push(a().toString(16));return i.join("");function a(){return t?15&t[r++]:16*Math.random()|0}}},2053:(e,t,r)=>{"use strict";r.d(t,{nb:()=>c,os:()=>u,yf:()=>s,zO:()=>a});var n=r(7145),i=(new Date).getTime(),o=i;function a(){return n.G&&performance.now?Math.round(performance.now()):(i=Math.max((new Date).getTime(),i))-o}function s(){return i}function c(e){o=e}function u(){return o}},7145:(e,t,r)=>{"use strict";r.d(t,{G:()=>n});const n=void 0!==r(2374)._A?.performance?.timing?.navigationStart},6625:(e,t,r)=>{"use strict";r.d(t,{s:()=>c,v:()=>u});var n=r(8283),i=r(9071),o=r(2053),a=r(7145),s=r(2374);let c=!0;function u(e){var t=function(){if(i.I&&i.I<9)return;if(a.G)return c=!1,s._A?.performance?.timing?.navigationStart}();t&&((0,n.B)(e,"starttime",t),(0,o.nb)(t))}},8283:(e,t,r)=>{"use strict";r.d(t,{B:()=>o,L:()=>a});var n=r(2053),i={};function o(e,t,r){void 0===r&&(r=(0,n.zO)()+(0,n.os)()),i[e]=i[e]||{},i[e][t]=r}function a(e,t,r,n){const o=e.sharedContext.agentIdentifier;var a=i[o]?.[r],s=i[o]?.[n];void 0!==a&&void 0!==s&&e.store("measures",t,{value:s-a})}},6368:(e,t,r)=>{"use strict";r.d(t,{e:()=>o});var n=r(2374),i={};function o(e){if(e in i)return i[e];if(0===(e||"").indexOf("data:"))return{protocol:"data"};let t;var r=n._A?.location,o={};if(n.il)t=document.createElement("a"),t.href=e;else try{t=new URL(e,r.href)}catch(e){return o}o.port=t.port;var a=t.href.split("://");!o.port&&a[1]&&(o.port=a[1].split("/")[0].split("@").pop().split(":")[1]),o.port&&"0"!==o.port||(o.port="https"===a[0]?"443":"80"),o.hostname=t.hostname||r.hostname,o.pathname=t.pathname,o.protocol=a[0],"/"!==o.pathname.charAt(0)&&(o.pathname="/"+o.pathname);var s=!t.protocol||":"===t.protocol||t.protocol===r.protocol,c=t.hostname===r.hostname&&t.port===r.port;return o.sameOrigin=s&&(!t.hostname||c),"/"===o.pathname&&(i[e]=o),o}},9548:(e,t,r)=>{"use strict";r.d(t,{T:()=>i});var n=r(2374);const i={isFileProtocol:function(){let e=Boolean("file:"===(0,n.lW)()?.location?.protocol);e&&(i.supportabilityMetricSent=!0);return e},supportabilityMetricSent:!1}},8610:(e,t,r)=>{"use strict";function n(e,t){console&&console.warn&&"function"==typeof console.warn&&(console.warn("New Relic: ".concat(e)),t&&console.warn(t))}r.d(t,{Z:()=>n})},3916:(e,t,r)=>{"use strict";r.d(t,{X:()=>i});var n=Object.prototype.hasOwnProperty;function i(e,t,r){if(n.call(e,t))return e[t];var i=r();if(Object.defineProperty&&Object.keys)try{return Object.defineProperty(e,t,{value:i,writable:!0,enumerable:!1}),i}catch(e){}return e[t]=i,i}},2374:(e,t,r)=>{"use strict";r.d(t,{_A:()=>o,il:()=>n,lW:()=>a,v6:()=>i});const n=Boolean("undefined"!=typeof window&&window.document),i=Boolean("undefined"!=typeof WorkerGlobalScope&&self.navigator instanceof WorkerNavigator);let o=(()=>{if(n)return window;if(i){if("undefined"!=typeof globalThis&&globalThis instanceof WorkerGlobalScope)return globalThis;if(self instanceof WorkerGlobalScope)return self}throw new Error('New Relic browser agent shutting down due to error: Unable to locate global scope. This is possibly due to code redefining browser global variables like "self" and "window".')})();function a(){return o}},7022:(e,t,r)=>{"use strict";r.d(t,{D:()=>i});var n=Object.prototype.hasOwnProperty;function i(e,t){var r=[],i="",o=0;for(i in e)n.call(e,i)&&(r[o]=t(i,e[i]),o+=1);return r}},9226:(e,t,r)=>{"use strict";r.d(t,{$c:()=>u,Ng:()=>d,RR:()=>c});var n=r(6562),i=r(9557),o=r(9548),a=r(8610),s={regex:/^file:\/\/(.*)/,replacement:"file://OBFUSCATED"};class c extends i.w{constructor(e){super(e)}shouldObfuscate(){return u(this.sharedContext.agentIdentifier).length>0}obfuscateString(e){if(!e||"string"!=typeof e)return e;for(var t=u(this.sharedContext.agentIdentifier),r=e,n=0;n<t.length;n++){var i=t[n].regex,o=t[n].replacement||"*";r=r.replace(i,o)}return r}}function u(e){var t=[],r=(0,n.Mt)(e,"obfuscate")||[];return t=t.concat(r),o.T.isFileProtocol()&&t.push(s),t}function d(e){for(var t=!1,r=!1,n=0;n<e.length;n++){"regex"in e[n]?"string"!=typeof e[n].regex&&e[n].regex.constructor!==RegExp&&((0,a.Z)('An obfuscation replacement rule contains a "regex" value with an invalid type (must be a string or RegExp)'),r=!0):((0,a.Z)('An obfuscation replacement rule was detected missing a "regex" value.'),r=!0);var i=e[n].replacement;i&&"string"!=typeof i&&((0,a.Z)('An obfuscation replacement rule contains a "replacement" value with an invalid type (must be a string)'),t=!0)}return!t&&!r}},2650:(e,t,r)=>{"use strict";r.d(t,{K:()=>a,b:()=>o});var n=r(8544);function i(){return"undefined"==typeof document||"complete"===document.readyState}function o(e,t){if(i())return e();(0,n.bP)("load",e,t)}function a(e){if(i())return e();(0,n.iz)("DOMContentLoaded",e)}},6797:(e,t,r)=>{"use strict";r.d(t,{EZ:()=>u,Qy:()=>c,ce:()=>o,fP:()=>a,gG:()=>d,mF:()=>s});var n=r(2053),i=r(2374);const o={beacon:"bam.nr-data.net",errorBeacon:"bam.nr-data.net"};function a(){return i._A.NREUM||(i._A.NREUM={}),void 0===i._A.newrelic&&(i._A.newrelic=i._A.NREUM),i._A.NREUM}function s(){let e=a();return e.o||(e.o={ST:i._A.setTimeout,SI:i._A.setImmediate,CT:i._A.clearTimeout,XHR:i._A.XMLHttpRequest,REQ:i._A.Request,EV:i._A.Event,PR:i._A.Promise,MO:i._A.MutationObserver,FETCH:i._A.fetch}),e}function c(e,t,r){let i=a();const o=i.initializedAgents||{},s=o[e]||{};return Object.keys(s).length||(s.initializedAt={ms:(0,n.zO)(),date:new Date}),i.initializedAgents={...o,[e]:{...s,[r]:t}},i}function u(e,t){a()[e]=t}function d(){return function(){let e=a();const t=e.info||{};e.info={beacon:o.beacon,errorBeacon:o.errorBeacon,...t}}(),function(){let e=a();const t=e.init||{};e.init={...t}}(),s(),function(){let e=a();const t=e.loader_config||{};e.loader_config={...t}}(),a()}},6998:(e,t,r)=>{"use strict";r.d(t,{N:()=>i,e:()=>o});var n=r(8544);function i(e){let t=arguments.length>1&&void 0!==arguments[1]&&arguments[1];return void(0,n.iz)("visibilitychange",(function(){if(t){if("hidden"!=document.visibilityState)return;e()}e(document.visibilityState)}))}function o(){return"hidden"===document.visibilityState?-1:1/0}},6408:(e,t,r)=>{"use strict";r.d(t,{W:()=>i});var n=r(2374);function i(){return"function"==typeof n._A?.PerformanceObserver}},7264:(e,t,r)=>{"use strict";r.d(t,{hF:()=>pe,Fp:()=>O,lx:()=>G,ow:()=>Y,ao:()=>te,G8:()=>oe,XV:()=>z,Zw:()=>N,ig:()=>we,em:()=>le,u5:()=>x,QU:()=>V,_L:()=>$,Gm:()=>ee,Lg:()=>ie,gy:()=>M,BV:()=>C,Kf:()=>ye});var n=r(3752),i=r(8683),o=r.n(i),a=r(2374);const s="nr@original";var c=Object.prototype.hasOwnProperty,u=!1;function d(e,t){return e||(e=n.ee),r.inPlace=function(e,t,n,i,o){n||(n="");var a,s,c,u="-"===n.charAt(0);for(c=0;c<t.length;c++)h(a=e[s=t[c]])||(e[s]=r(a,u?s+n:n,i,s,o))},r.flag=s,r;function r(t,r,n,a,c){return h(t)?t:(r||(r=""),nrWrapper[s]=t,l(t,nrWrapper,e),nrWrapper);function nrWrapper(){var s,u,d,l;try{u=this,s=o()(arguments),d="function"==typeof n?n(s,u):n||{}}catch(t){f([t,"",[s,u,a],d],e)}i(r+"start",[s,u,a],d,c);try{return l=t.apply(u,s)}catch(e){throw i(r+"err",[s,u,e],d,c),e}finally{i(r+"end",[s,u,l],d,c)}}}function i(r,n,i,o){if(!u||t){var a=u;u=!0;try{e.emit(r,n,i,t,o)}catch(t){f([t,r,n,i],e)}u=a}}}function f(e,t){t||(t=n.ee);try{t.emit("internal-error",e)}catch(e){}}function l(e,t,r){if(Object.defineProperty&&Object.keys)try{return Object.keys(e).forEach((function(r){Object.defineProperty(t,r,{get:function(){return e[r]},set:function(t){return e[r]=t,t}})})),t}catch(e){f([e],r)}for(var n in e)c.call(e,n)&&(t[n]=e[n]);return t}function h(e){return!(e&&e instanceof Function&&e.apply&&!e[s])}function p(e,t){e?.[t]?.[s]&&(e[t]=e[t][s])}var g="fetch-",v=g+"body-",m=["arrayBuffer","blob","json","text","formData"],b=a._A.Request,y=a._A.Response,w="prototype",E="nr@context";const A={};function x(e){const t=T(e);if(!(b&&y&&a._A.fetch))return t;if(A[t.debugId]++)return t;function r(e,r,n){var i=e[r];"function"==typeof i&&(e[r]=function(){var e,r=o()(arguments),s={};t.emit(n+"before-start",[r],s),s[E]&&s[E].dt&&(e=s[E].dt);var c=i.apply(this,r);return t.emit(n+"start",[r,e],c),a._A.Promise.resolve(c).then((function(e){return t.emit(n+"end",[null,e],c),e}),(function(e){throw t.emit(n+"end",[e],c),e}))},e[r][s]=i)}return A[t.debugId]=1,m.forEach((e=>{r(b[w],e,v),r(y[w],e,v)})),r(a._A,"fetch",g),t.on(g+"end",(function(e,r){var n=this;if(r){var i=r.headers.get("content-length");null!==i&&(n.rxSize=i),t.emit(g+"done",[null,r],n)}else t.emit(g+"done",[e],n)})),t}function O(e){const t=T(e);1==A[t.debugId]?(m.forEach((e=>{p(b[w],e),p(y[w],e)})),p(a._A,"fetch"),A[t.debugId]=1/0):A[t.debugId]--}function T(e){return(e||n.ee).get("fetch")}const S={},_="setTimeout",I="setInterval",P="clearTimeout",j="-start",R="-",D=[_,"setImmediate",I,P,"clearImmediate"];function C(e){const t=k(e);if(S[t.debugId]++)return t;S[t.debugId]=1;var r=d(t);return r.inPlace(a._A,D.slice(0,2),_+R),r.inPlace(a._A,D.slice(2,3),I+R),r.inPlace(a._A,D.slice(3),P+R),t.on(I+j,(function(e,t,n){e[0]=r(e[0],"fn-",null,n)})),t.on(_+j,(function(e,t,n){this.method=n,this.timerDuration=isNaN(e[1])?0:+e[1],e[0]=r(e[0],"fn-",this,n)})),t}function N(e){const t=k(e);1==S[t.debugId]?(D.forEach((e=>p(a._A,e))),S[t.debugId]=1/0):S[t.debugId]--}function k(e){return(e||n.ee).get("timer")}const L={},H="requestAnimationFrame";function M(e){const t=B(e);if(!a.il||L[t.debugId]++)return t;L[t.debugId]=1;var r=d(t);return r.inPlace(window,[H],"raf-"),t.on("raf-start",(function(e){e[0]=r(e[0],"fn-")})),t}function z(e){const t=B(e);1==L[t.debugId]?(p(window,H),L[t.debugId]=1/0):L[t.debugId]--}function B(e){return(e||n.ee).get("raf")}const U={},F=["pushState","replaceState"];function V(e){const t=q(e);return!a.il||U[t.debugId]++||(U[t.debugId]=1,d(t).inPlace(window.history,F,"-")),t}function G(e){const t=q(e);1==U[t.debugId]?(F.forEach((e=>p(window.history,e))),U[t.debugId]=1/0):U[t.debugId]--}function q(e){return(e||n.ee).get("history")}var W=r(8544);const X={},Z=["appendChild","insertBefore","replaceChild"];function $(e){const t=Q(e);if(!a.il||X[t.debugId])return t;X[t.debugId]=!0;var r=d(t),n=/[?&](?:callback|cb)=([^&#]+)/,i=/(.*)\.([^.]+)/,o=/^(\w+)(\.|$)(.*)$/;function s(e,t){var r=e.match(o),n=r[1],i=r[3];return i?s(i,t[n]):t[n]}return r.inPlace(Node.prototype,Z,"dom-"),t.on("dom-start",(function(e){!function(e){if(!e||"string"!=typeof e.nodeName||"script"!==e.nodeName.toLowerCase())return;if("function"!=typeof e.addEventListener)return;var o=(a=e.src,c=a.match(n),c?c[1]:null);var a,c;if(!o)return;var u=function(e){var t=e.match(i);if(t&&t.length>=3)return{key:t[2],parent:s(t[1],window)};return{key:e,parent:window}}(o);if("function"!=typeof u.parent[u.key])return;var d={};function f(){t.emit("jsonp-end",[],d),e.removeEventListener("load",f,(0,W.m$)(!1)),e.removeEventListener("error",l,(0,W.m$)(!1))}function l(){t.emit("jsonp-error",[],d),t.emit("jsonp-end",[],d),e.removeEventListener("load",f,(0,W.m$)(!1)),e.removeEventListener("error",l,(0,W.m$)(!1))}r.inPlace(u.parent,[u.key],"cb-",d),e.addEventListener("load",f,(0,W.m$)(!1)),e.addEventListener("error",l,(0,W.m$)(!1)),t.emit("new-jsonp",[e.src],d)}(e[0])})),t}function Y(e){const t=Q(e);!0===X[t.debugId]&&(Z.forEach((e=>p(Node.prototype,e))),X[t.debugId]="unwrapped")}function Q(e){return(e||n.ee).get("jsonp")}var K=r(6562);const J={};function ee(e){const t=re(e);if(!a.il||J[t.debugId])return t;J[t.debugId]=!0;var r=d(t),n=K.Yu.MO;return n&&(window.MutationObserver=function(e){return this instanceof n?new n(r(e,"fn-")):n.apply(this,arguments)},MutationObserver.prototype=n.prototype),t}function te(e){const t=re(e);!0===J[t.debugId]&&(window.MutationObserver=K.Yu.MO,J[t.debugId]="unwrapped")}function re(e){return(e||n.ee).get("mutation")}const ne={};function ie(e){const t=ae(e);if(ne[t.debugId])return t;ne[t.debugId]=!0;var r=n.c,i=d(t),o=K.Yu.PR;return o&&function(){function e(r){var n=t.context(),a=i(r,"executor-",n,null,!1);const s=Reflect.construct(o,[a],e);return t.context(s).getCtx=function(){return n},s}a._A.Promise=e,Object.defineProperty(e,"name",{value:"Promise"}),e.toString=function(){return o.toString()},Object.setPrototypeOf(e,o),["all","race"].forEach((function(r){const n=o[r];e[r]=function(e){let i=!1;e?.forEach((e=>{this.resolve(e).then(a("all"===r),a(!1))}));const o=n.apply(this,arguments);return o;function a(e){return function(){t.emit("propagate",[null,!i],o,!1,!1),i=i||!e}}}})),["resolve","reject"].forEach((function(r){const n=o[r];e[r]=function(e){const r=n.apply(this,arguments);return e!==r&&t.emit("propagate",[e,!0],r,!1,!1),r}})),e.prototype=Object.create(o.prototype),e.prototype.constructor=e,e.prototype.then=function(){var e=this,n=r(e);n.promise=e;for(var a=arguments.length,s=new Array(a),c=0;c<a;c++)s[c]=arguments[c];s[0]=i(s[0],"cb-",n,null,!1),s[1]=i(s[1],"cb-",n,null,!1);const u=o.prototype.then.apply(this,s);return n.nextPromise=u,t.emit("propagate",[e,!0],u,!1,!1),u},t.on("executor-start",(function(e){e[0]=i(e[0],"resolve-",this,null,!1),e[1]=i(e[1],"resolve-",this,null,!1)})),t.on("executor-err",(function(e,t,r){e[1](r)})),t.on("cb-end",(function(e,r,n){t.emit("propagate",[n,!0],this.nextPromise,!1,!1)})),t.on("propagate",(function(e,r,n){this.getCtx&&!r||(this.getCtx=function(){if(e instanceof Promise)var r=t.context(e);return r&&r.getCtx?r.getCtx():this})}))}(),t}function oe(e){const t=ae(e);!0===ne[t.debugId]&&(a._A.Promise=K.Yu.PR,ne[t.debugId]="unwrapped")}function ae(e){return(e||n.ee).get("promise")}var se=r(3916);const ce={},ue=XMLHttpRequest,de="addEventListener",fe="removeEventListener";function le(e){var t=ge(e);if(ce[t.debugId]++)return t;ce[t.debugId]=1;var r=d(t,!0);function n(e){r.inPlace(e,[de,fe],"-",i)}function i(e,t){return e[1]}return"getPrototypeOf"in Object&&(a.il&&he(document,n),he(a._A,n),he(ue.prototype,n)),t.on(de+"-start",(function(e,t){var n=e[1];if(null!==n&&("function"==typeof n||"object"==typeof n)){var i=(0,se.X)(n,"nr@wrapped",(function(){var e={object:function(){if("function"!=typeof n.handleEvent)return;return n.handleEvent.apply(n,arguments)},function:n}[typeof n];return e?r(e,"fn-",null,e.name||"anonymous"):n}));this.wrapped=e[1]=i}})),t.on(fe+"-start",(function(e){e[1]=this.wrapped||e[1]})),t}function he(e,t){let r=e;for(;"object"==typeof r&&!Object.prototype.hasOwnProperty.call(r,de);)r=Object.getPrototypeOf(r);for(var n=arguments.length,i=new Array(n>2?n-2:0),o=2;o<n;o++)i[o-2]=arguments[o];r&&t(r,...i)}function pe(e){const t=ge(e);1==ce[t.debugId]?([de,fe].forEach((e=>{"object"==typeof document&&he(document,p,e),he(a._A,p,e),he(ue.prototype,p,e)})),ce[t.debugId]=1/0):ce[t.debugId]--}function ge(e){return(e||n.ee).get("events")}var ve=r(8610);const me={},be=["open","send"];function ye(e){var t=e||n.ee;const r=Ee(t);if(me[r.debugId]++)return r;me[r.debugId]=1,le(t);var i=d(r),o=K.Yu.XHR,s=K.Yu.MO,c=K.Yu.PR,u=K.Yu.SI,f="readystatechange",l=["onload","onerror","onabort","onloadstart","onloadend","onprogress","ontimeout"],h=[],p=a._A.XMLHttpRequest.listeners,g=a._A.XMLHttpRequest=function(e){var t=new o(e);function n(){try{r.emit("new-xhr",[t],t),t.addEventListener(f,m,(0,W.m$)(!1))}catch(e){(0,ve.Z)("An error occured while intercepting XHR",e);try{r.emit("internal-error",[e])}catch(e){}}}return this.listeners=p?[...p,n]:[n],this.listeners.forEach((e=>e())),t};function v(e,t){i.inPlace(t,["onreadystatechange"],"fn-",A)}function m(){var e=this,t=r.context(e);e.readyState>3&&!t.resolved&&(t.resolved=!0,r.emit("xhr-resolved",[],e)),i.inPlace(e,l,"fn-",A)}if(function(e,t){for(var r in e)t[r]=e[r]}(o,g),g.prototype=o.prototype,i.inPlace(g.prototype,be,"-xhr-",A),r.on("send-xhr-start",(function(e,t){v(e,t),function(e){h.push(e),s&&(b?b.then(E):u?u(E):(y=-y,w.data=y))}(t)})),r.on("open-xhr-start",v),s){var b=c&&c.resolve();if(!u&&!c){var y=1,w=document.createTextNode(y);new s(E).observe(w,{characterData:!0})}}else t.on("fn-end",(function(e){e[0]&&e[0].type===f||E()}));function E(){for(var e=0;e<h.length;e++)v(0,h[e]);h.length&&(h=[])}function A(e,t){return t}return r}function we(e){const t=Ee(e);1==me[t.debugId]?(pe(t),a._A.XMLHttpRequest=K.Yu.XHR,be.forEach((e=>{p(a._A.XMLHttpRequest.prototype,e)})),me[t.debugId]=1/0):me[t.debugId]--}function Ee(e){return(e||n.ee).get("xhr")}},8675:(e,t,r)=>{"use strict";r.d(t,{t:()=>n});const n=r(2325).D.ajax},948:(e,t,r)=>{"use strict";r.r(t),r.d(t,{Instrument:()=>j});var n=r(6562),i=r(9252),o=r(3916),a=r(2374),s=1,c="nr@id";function u(e){var t=typeof e;return!e||"object"!==t&&"function"!==t?-1:e===a._A?0:(0,o.X)(e,c,(function(){return s++}))}var d=r(9071);function f(e){if("string"==typeof e&&e.length)return e.length;if("object"==typeof e){if("undefined"!=typeof ArrayBuffer&&e instanceof ArrayBuffer&&e.byteLength)return e.byteLength;if("undefined"!=typeof Blob&&e instanceof Blob&&e.size)return e.size;if(!("undefined"!=typeof FormData&&e instanceof FormData))try{return JSON.stringify(e).length}catch(e){return}}}var l=r(8544),h=r(2053),p=r(7264),g=r(6368),v=r(5526);class m{constructor(e){this.agentIdentifier=e,this.generateTracePayload=this.generateTracePayload.bind(this),this.shouldGenerateTrace=this.shouldGenerateTrace.bind(this)}generateTracePayload(e){if(!this.shouldGenerateTrace(e))return null;var t=(0,n.DL)(this.agentIdentifier);if(!t)return null;var r=(t.accountID||"").toString()||null,i=(t.agentID||"").toString()||null,o=(t.trustKey||"").toString()||null;if(!r||!i)return null;var a=(0,v.M)(),s=(0,v.Ht)(),c=Date.now(),u={spanId:a,traceId:s,timestamp:c};return(e.sameOrigin||this.isAllowedOrigin(e)&&this.useTraceContextHeadersForCors())&&(u.traceContextParentHeader=this.generateTraceContextParentHeader(a,s),u.traceContextStateHeader=this.generateTraceContextStateHeader(a,c,r,i,o)),(e.sameOrigin&&!this.excludeNewrelicHeader()||!e.sameOrigin&&this.isAllowedOrigin(e)&&this.useNewrelicHeaderForCors())&&(u.newrelicHeader=this.generateTraceHeader(a,s,c,r,i,o)),u}generateTraceContextParentHeader(e,t){return"00-"+t+"-"+e+"-01"}generateTraceContextStateHeader(e,t,r,n,i){return i+"@nr=0-1-"+r+"-"+n+"-"+e+"----"+t}generateTraceHeader(e,t,r,n,i,o){if(!("function"==typeof a._A?.btoa))return null;var s={v:[0,1],d:{ty:"Browser",ac:n,ap:i,id:e,tr:t,ti:r}};return o&&n!==o&&(s.d.tk=o),btoa(JSON.stringify(s))}shouldGenerateTrace(e){return this.isDtEnabled()&&this.isAllowedOrigin(e)}isAllowedOrigin(e){var t=!1,r={};if((0,n.Mt)(this.agentIdentifier,"distributed_tracing")&&(r=(0,n.P_)(this.agentIdentifier).distributed_tracing),e.sameOrigin)t=!0;else if(r.allowed_origins instanceof Array)for(var i=0;i<r.allowed_origins.length;i++){var o=(0,g.e)(r.allowed_origins[i]);if(e.hostname===o.hostname&&e.protocol===o.protocol&&e.port===o.port){t=!0;break}}return t}isDtEnabled(){var e=(0,n.Mt)(this.agentIdentifier,"distributed_tracing");return!!e&&!!e.enabled}excludeNewrelicHeader(){var e=(0,n.Mt)(this.agentIdentifier,"distributed_tracing");return!!e&&!!e.exclude_newrelic_header}useNewrelicHeaderForCors(){var e=(0,n.Mt)(this.agentIdentifier,"distributed_tracing");return!!e&&!1!==e.cors_use_newrelic_header}useTraceContextHeadersForCors(){var e=(0,n.Mt)(this.agentIdentifier,"distributed_tracing");return!!e&&!!e.cors_use_tracecontext_headers}}var b=r(6114),y=r(8675),w=r(2325);function E(e,t){!function(e,t){if(t.has(e))throw new TypeError("Cannot initialize the same private elements twice on an object")}(e,t),t.add(e)}var A,x,O,T=["load","error","abort","timeout"],S=T.length,_=n.Yu.REQ,I=a._A.XMLHttpRequest,P=new WeakSet;class j extends b.S{constructor(e,t){let r=!(arguments.length>2&&void 0!==arguments[2])||arguments[2];super(e,t,y.t,r),E(this,P),(0,n.OP)(e).xhrWrappable&&(this.dt=new m(e),this.handler=(e,t,r,n)=>(0,i.p)(e,t,r,n,this.ee),(0,p.u5)(this.ee),(0,p.Kf)(this.ee),function(e,t,r,i){function o(e){var t=this;t.totalCbs=0,t.called=0,t.cbTime=0,t.end=D,t.ended=!1,t.xhrGuids={},t.lastSize=null,t.loadCaptureCalled=!1,t.params=this.params||{},t.metrics=this.metrics||{},e.addEventListener("load",(function(r){N(t,e)}),(0,l.m$)(!1)),d.I||e.addEventListener("progress",(function(e){t.lastSize=e.loaded}),(0,l.m$)(!1))}function s(e){this.params={method:e[0]},C(this,e[1]),this.metrics={}}function c(t,r){var o=(0,n.DL)(e);"xpid"in o&&this.sameOrigin&&r.setRequestHeader("X-NewRelic-ID",o.xpid);var a=i.generateTracePayload(this.parsedOrigin);if(a){var s=!1;a.newrelicHeader&&(r.setRequestHeader("newrelic",a.newrelicHeader),s=!0),a.traceContextParentHeader&&(r.setRequestHeader("traceparent",a.traceContextParentHeader),a.traceContextStateHeader&&r.setRequestHeader("tracestate",a.traceContextStateHeader),s=!0),s&&(this.dt=a)}}function p(e,r){var n=this.metrics,i=e[0],o=this;if(n&&i){var a=f(i);a&&(n.txSize=a)}this.startTime=(0,h.zO)(),this.listener=function(e){try{"abort"!==e.type||o.loadCaptureCalled||(o.params.aborted=!0),("load"!==e.type||o.called===o.totalCbs&&(o.onloadCalled||"function"!=typeof r.onload)&&"function"==typeof o.end)&&o.end(r)}catch(e){try{t.emit("internal-error",[e])}catch(e){}}};for(var s=0;s<S;s++)r.addEventListener(T[s],this.listener,(0,l.m$)(!1))}function v(e,t,r){this.cbTime+=e,t?this.onloadCalled=!0:this.called+=1,this.called!==this.totalCbs||!this.onloadCalled&&"function"==typeof r.onload||"function"!=typeof this.end||this.end(r)}function m(e,t){var r=""+u(e)+!!t;this.xhrGuids&&!this.xhrGuids[r]&&(this.xhrGuids[r]=!0,this.totalCbs+=1)}function b(e,t){var r=""+u(e)+!!t;this.xhrGuids&&this.xhrGuids[r]&&(delete this.xhrGuids[r],this.totalCbs-=1)}function y(){this.endTime=(0,h.zO)()}function E(e,r){r instanceof I&&"load"===e[0]&&t.emit("xhr-load-added",[e[1],e[2]],r)}function A(e,r){r instanceof I&&"load"===e[0]&&t.emit("xhr-load-removed",[e[1],e[2]],r)}function x(e,t,r){t instanceof I&&("onload"===r&&(this.onload=!0),("load"===(e[0]&&e[0].type)||this.onload)&&(this.xhrCbStart=(0,h.zO)()))}function O(e,r){this.xhrCbStart&&t.emit("xhr-cb-time",[(0,h.zO)()-this.xhrCbStart,this.onload,r],r)}function P(e){var t,r=e[1]||{};"string"==typeof e[0]?t=e[0]:e[0]&&e[0].url?t=e[0].url:a._A?.URL&&e[0]&&e[0]instanceof URL&&(t=e[0].href),t&&(this.parsedOrigin=(0,g.e)(t),this.sameOrigin=this.parsedOrigin.sameOrigin);var n=i.generateTracePayload(this.parsedOrigin);if(n&&(n.newrelicHeader||n.traceContextParentHeader))if("string"==typeof e[0]||a._A?.URL&&e[0]&&e[0]instanceof URL){var o={};for(var s in r)o[s]=r[s];o.headers=new Headers(r.headers||{}),c(o.headers,n)&&(this.dt=n),e.length>1?e[1]=o:e.push(o)}else e[0]&&e[0].headers&&c(e[0].headers,n)&&(this.dt=n);function c(e,t){var r=!1;return t.newrelicHeader&&(e.set("newrelic",t.newrelicHeader),r=!0),t.traceContextParentHeader&&(e.set("traceparent",t.traceContextParentHeader),t.traceContextStateHeader&&e.set("tracestate",t.traceContextStateHeader),r=!0),r}}function j(e,t){this.params={},this.metrics={},this.startTime=(0,h.zO)(),this.dt=t,e.length>=1&&(this.target=e[0]),e.length>=2&&(this.opts=e[1]);var r,n=this.opts||{},i=this.target;"string"==typeof i?r=i:"object"==typeof i&&i instanceof _?r=i.url:a._A?.URL&&"object"==typeof i&&i instanceof URL&&(r=i.href),C(this,r);var o=(""+(i&&i instanceof _&&i.method||n.method||"GET")).toUpperCase();this.params.method=o,this.txSize=f(n.body)||0}function R(e,t){var n;this.endTime=(0,h.zO)(),this.params||(this.params={}),this.params.status=t?t.status:0,"string"==typeof this.rxSize&&this.rxSize.length>0&&(n=+this.rxSize);var i={txSize:this.txSize,rxSize:n,duration:(0,h.zO)()-this.startTime};r("xhr",[this.params,i,this.startTime,this.endTime,"fetch"],this,w.D.ajax)}function D(e){var t=this.params,n=this.metrics;if(!this.ended){this.ended=!0;for(var i=0;i<S;i++)e.removeEventListener(T[i],this.listener,!1);t.aborted||(n.duration=(0,h.zO)()-this.startTime,this.loadCaptureCalled||4!==e.readyState?null==t.status&&(t.status=0):N(this,e),n.cbTime=this.cbTime,r("xhr",[t,n,this.startTime,this.endTime,"xhr"],this,w.D.ajax))}}function C(e,t){var r=(0,g.e)(t),n=e.params;n.hostname=r.hostname,n.port=r.port,n.protocol=r.protocol,n.host=r.hostname+":"+r.port,n.pathname=r.pathname,e.parsedOrigin=r,e.sameOrigin=r.sameOrigin}function N(e,t){e.params.status=t.status;var r=function(e,t){var r=e.responseType;return"json"===r&&null!==t?t:"arraybuffer"===r||"blob"===r||"json"===r?f(e.response):"text"===r||""===r||void 0===r?f(e.responseText):void 0}(t,e.lastSize);if(r&&(e.metrics.rxSize=r),e.sameOrigin){var n=t.getResponseHeader("X-NewRelic-App-Data");n&&(e.params.cat=n.split(", ").pop())}e.loadCaptureCalled=!0}t.on("new-xhr",o),t.on("open-xhr-start",s),t.on("open-xhr-end",c),t.on("send-xhr-start",p),t.on("xhr-cb-time",v),t.on("xhr-load-added",m),t.on("xhr-load-removed",b),t.on("xhr-resolved",y),t.on("addEventListener-end",E),t.on("removeEventListener-end",A),t.on("fn-end",O),t.on("fetch-before-start",P),t.on("fetch-start",j),t.on("fn-start",x),t.on("fetch-done",R)}(e,this.ee,this.handler,this.dt),this.abortHandler=function(e,t,r){if(!t.has(e))throw new TypeError("attempted to get private field on non-instance");return r}(this,P,R),this.importAggregator())}}function R(){(0,p.Fp)(this.ee),(0,p.ig)(this.ee),this.abortHandler=void 0}A=j,x="featureName",O=y.t,(x=function(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}(x))in A?Object.defineProperty(A,x,{value:O,enumerable:!0,configurable:!0,writable:!0}):A[x]=O},8322:(e,t,r)=>{"use strict";r.d(t,{A:()=>i,t:()=>n});const n=r(2325).D.jserrors,i="nr@seenError"},9715:(e,t,r)=>{"use strict";r.r(t),r.d(t,{Instrument:()=>T});var n,i=r(9252),o=r(2053),a=r(3916),s=r(7264),c=r(8683),u=r.n(c),d=r(3752),f=r(7022),l={};try{n=localStorage.getItem("__nr_flags").split(","),console&&"function"==typeof console.log&&(l.console=!0,-1!==n.indexOf("dev")&&(l.dev=!0),-1!==n.indexOf("nr_dev")&&(l.nrDev=!0))}catch(e){}function h(e){try{l.console&&h(e)}catch(e){}}l.nrDev&&d.ee.on("internal-error",(function(e){h(e.stack)})),l.dev&&d.ee.on("fn-err",(function(e,t,r){h(r.stack)})),l.dev&&(h("NR AGENT IN DEVELOPMENT MODE"),h("flags: "+(0,f.D)(l,(function(e,t){return e})).join(", ")));var p=r(6114),g=r(8322),v=r(2325),m=r(2374),b=r(8544),y=r(6562);function w(e,t){!function(e,t){if(t.has(e))throw new TypeError("Cannot initialize the same private elements twice on an object")}(e,t),t.add(e)}var E,A,x,O=new WeakSet;class T extends p.S{constructor(e,t){var r;let n=!(arguments.length>2&&void 0!==arguments[2])||arguments[2];super(e,t,g.t,n),r=this,w(this,O),this.skipNext=0,this.origOnerror=m._A.onerror;try{this.removeOnAbort=new AbortController}catch(e){}const c=this;c.ee.on("fn-start",(function(e,t,r){c.abortHandler&&(c.skipNext+=1)})),c.ee.on("fn-err",(function(e,t,r){c.abortHandler&&!r[g.A]&&((0,a.X)(r,g.A,(function(){return!0})),this.thrown=!0,I(r,void 0,c.ee))})),c.ee.on("fn-end",(function(){c.abortHandler&&!this.thrown&&c.skipNext>0&&(c.skipNext-=1)})),c.ee.on("internal-error",(function(e){(0,i.p)("ierr",[e,(0,o.zO)(),!0],void 0,v.D.jserrors,c.ee)})),m._A.onerror=function(){return r.origOnerror&&r.origOnerror(...arguments),r.onerrorHandler(...arguments),!1},m._A.addEventListener("unhandledrejection",(e=>{const t=function(e){let t="Unhandled Promise Rejection: ";if(e instanceof Error)return e.message=t+e.message,e;if(void 0===e)return new Error(t);try{return new Error(t+JSON.stringify(e))}catch(e){return new Error(t)}}(e.reason);(0,i.p)("err",[t,(0,o.zO)(),!1,{unhandledPromiseRejection:1}],void 0,v.D.jserrors,this.ee)}),(0,b.m$)(!1,this.removeOnAbort?.signal)),(0,s.gy)(this.ee),(0,s.BV)(this.ee),(0,s.em)(this.ee),(0,y.OP)(e).xhrWrappable&&(0,s.Kf)(this.ee),this.abortHandler=function(e,t,r){if(!t.has(e))throw new TypeError("attempted to get private field on non-instance");return r}(this,O,S),this.importAggregator()}onerrorHandler(e,t,r,n,a){try{this.skipNext?this.skipNext-=1:I(a||new _(e,t,r),!0,this.ee)}catch(e){try{(0,i.p)("ierr",[e,(0,o.zO)(),!0],void 0,v.D.jserrors,this.ee)}catch(e){}}return"function"==typeof this.origOnerror&&this.origOnerror.apply(this,u()(arguments))}}function S(){m._A.onerror=this.origOnerror,this.removeOnAbort?.abort(),(0,s.XV)(this.ee),(0,s.Zw)(this.ee),(0,s.hF)(this.ee),(0,y.OP)(this.agentIdentifier).xhrWrappable&&(0,s.ig)(this.ee),this.abortHandler=void 0}function _(e,t,r){this.message=e||"Uncaught error with no additional information",this.sourceURL=t,this.line=r}function I(e,t,r){var n=t?null:(0,o.zO)();(0,i.p)("err",[e,n],void 0,v.D.jserrors,r)}E=T,A="featureName",x=g.t,(A=function(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}(A))in E?Object.defineProperty(E,A,{value:x,enumerable:!0,configurable:!0,writable:!0}):E[A]=x},6034:(e,t,r)=>{"use strict";r.d(t,{t:()=>n});const n=r(2325).D.metrics},600:(e,t,r)=>{"use strict";r.r(t),r.d(t,{Instrument:()=>O,constants:()=>T});var n=r(9252),i=r(4045),o=r(6114),a=r(2374),s={REACT:"React",ANGULAR:"Angular",ANGULARJS:"AngularJS",BACKBONE:"Backbone",EMBER:"Ember",VUE:"Vue",METEOR:"Meteor",ZEPTO:"Zepto",JQUERY:"Jquery"};function c(){if(!a.il)return[];var e=[];try{(function(){try{if(window.React||window.ReactDOM||window.ReactRedux)return!0;if(document.querySelector("[data-reactroot], [data-reactid]"))return!0;for(var e=document.querySelectorAll("body > div"),t=0;t<e.length;t++)if(Object.keys(e[t]).indexOf("_reactRootContainer")>=0)return!0;return!1}catch(e){return!1}})()&&e.push(s.REACT),function(){try{return!!window.angular||(!!document.querySelector(".ng-binding, [ng-app], [data-ng-app], [ng-controller], [data-ng-controller], [ng-repeat], [data-ng-repeat]")||!!document.querySelector('script[src*="angular.js"], script[src*="angular.min.js"]'))}catch(e){return!1}}()&&e.push(s.ANGULARJS),function(){try{return!!(window.hasOwnProperty("ng")&&window.ng.hasOwnProperty("coreTokens")&&window.ng.coreTokens.hasOwnProperty("NgZone"))||!!document.querySelectorAll("[ng-version]").length}catch(e){return!1}}()&&e.push(s.ANGULAR),window.Backbone&&e.push(s.BACKBONE),window.Ember&&e.push(s.EMBER),window.Vue&&e.push(s.VUE),window.Meteor&&e.push(s.METEOR),window.Zepto&&e.push(s.ZEPTO),window.jQuery&&e.push(s.JQUERY)}catch(e){}return e}var u=r(9548),d=r(9226),f=r(8226),l=r(2650),h=r(8544),p=r(6562),g=r(8610);const v={dedicated:Boolean(a._A?.Worker),shared:Boolean(a._A?.SharedWorker),service:Boolean(a._A?.navigator?.serviceWorker)};let m,b,y;var w=r(6034);var E,A,x;class O extends o.S{constructor(e,t){var r;let n=!(arguments.length>2&&void 0!==arguments[2])||arguments[2];super(e,t,w.t,n),r=this,this.singleChecks(),this.eachSessionChecks(),(0,i.X)("record-supportability",(function(){return r.recordSupportability(...arguments)}),this.featureName,this.ee),(0,i.X)("record-custom",(function(){return r.recordCustom(...arguments)}),this.featureName,this.ee),this.importAggregator()}recordSupportability(e,t){var r=["sm",e,{name:e},t];return(0,n.p)("storeMetric",r,null,this.featureName,this.ee),r}recordCustom(e,t){var r=["cm",e,{name:e},t];return(0,n.p)("storeEventMetrics",r,null,this.featureName,this.ee),r}singleChecks(){this.recordSupportability("Generic/Version/".concat(f.q,"/Detected"));const{loaderType:e}=(0,p.OP)(this.agentIdentifier);e&&this.recordSupportability("Generic/LoaderType/".concat(e,"/Detected")),a.il&&(0,l.K)((()=>{c().forEach((e=>{this.recordSupportability("Framework/"+e+"/Detected")}))})),u.T.isFileProtocol()&&(this.recordSupportability("Generic/FileProtocol/Detected"),u.T.supportabilityMetricSent=!0);const t=(0,d.$c)(this.agentIdentifier);t.length>0&&this.recordSupportability("Generic/Obfuscate/Detected"),t.length>0&&!(0,d.Ng)(t)&&this.recordSupportability("Generic/Obfuscate/Invalid"),function(e){if(!m){if(v.dedicated){m=Worker;try{a._A.Worker=r(m,"Dedicated")}catch(e){o(e,"Dedicated")}if(v.shared){b=SharedWorker;try{a._A.SharedWorker=r(b,"Shared")}catch(e){o(e,"Shared")}}else n("Shared");if(v.service){y=navigator.serviceWorker.register;try{a._A.navigator.serviceWorker.register=(t=y,function(){for(var e=arguments.length,r=new Array(e),n=0;n<e;n++)r[n]=arguments[n];return i("Service",r[1]?.type),t.apply(navigator.serviceWorker,r)})}catch(e){o(e,"Service")}}else n("Service");var t;return}n("All")}function r(e,t){return"undefined"==typeof Proxy?e:new Proxy(e,{construct:(e,r)=>(i(t,r[1]?.type),new e(...r))})}function n(t){a.v6||e("Workers/".concat(t,"/Unavailable"))}function i(t,r){e("Workers/".concat(t,"module"===r?"/Module":"/Classic"))}function o(t,r){e("Workers/".concat(r,"/SM/Unsupported")),(0,g.Z)("NR Agent: Unable to capture ".concat(r," workers."),t)}}(this.recordSupportability.bind(this))}eachSessionChecks(){a.il&&(0,h.bP)("pageshow",(e=>{e.persisted&&this.recordSupportability("Generic/BFCache/PageRestored")}))}}E=O,A="featureName",x=w.t,(A=function(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}(A))in E?Object.defineProperty(E,A,{value:x,enumerable:!0,configurable:!0,writable:!0}):E[A]=x;var T={SUPPORTABILITY_METRIC:"sm",CUSTOM_METRIC:"cm"}},6486:(e,t,r)=>{"use strict";r.d(t,{t:()=>n});const n=r(2325).D.pageAction},488:(e,t,r)=>{"use strict";r.r(t),r.d(t,{Instrument:()=>c});var n,i,o,a=r(6114),s=r(6486);class c extends a.S{constructor(e,t){let r=!(arguments.length>2&&void 0!==arguments[2])||arguments[2];super(e,t,s.t,r),this.importAggregator()}}n=c,i="featureName",o=s.t,(i=function(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}(i))in n?Object.defineProperty(n,i,{value:o,enumerable:!0,configurable:!0,writable:!0}):n[i]=o},2484:(e,t,r)=>{"use strict";r.d(t,{t:()=>n});const n=r(2325).D.pageViewEvent},5637:(e,t,r)=>{"use strict";r.r(t),r.d(t,{Instrument:()=>g});var n,i,o,a=r(9252),s=r(2053),c=r(8283),u=r(6625),d=r(6114),f=r(2650),l=r(2484),h=r(2325),p=r(2374);class g extends d.S{constructor(e,t){let r=!(arguments.length>2&&void 0!==arguments[2])||arguments[2];super(e,t,l.t,r),p.il&&((0,u.v)(e),(0,c.B)(e,"firstbyte",(0,s.yf)()),(0,f.K)((()=>this.measureDomContentLoaded())),(0,f.b)((()=>this.measureWindowLoaded()),!0),this.importAggregator())}measureWindowLoaded(){var e=(0,s.zO)();(0,c.B)(this.agentIdentifier,"onload",e+(0,s.os)()),(0,a.p)("timing",["load",e],void 0,h.D.pageViewTiming,this.ee)}measureDomContentLoaded(){(0,c.B)(this.agentIdentifier,"domContent",(0,s.zO)()+(0,s.os)())}}n=g,i="featureName",o=l.t,(i=function(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}(i))in n?Object.defineProperty(n,i,{value:o,enumerable:!0,configurable:!0,writable:!0}):n[i]=o},6382:(e,t,r)=>{"use strict";r.d(t,{t:()=>n});const n=r(2325).D.pageViewTiming},7817:(e,t,r)=>{"use strict";r.r(t),r.d(t,{Instrument:()=>g});var n,i,o,a=r(9252),s=r(6998),c=r(8544),u=r(2053),d=r(6562),f=r(6114),l=r(6382),h=r(2325),p=r(2374);class g extends f.S{constructor(e,t){var r;let n=!(arguments.length>2&&void 0!==arguments[2])||arguments[2];if(super(e,t,l.t,n),r=this,p.il){if(this.pageHiddenTime=(0,s.e)(),this.performanceObserver,this.lcpPerformanceObserver,this.clsPerformanceObserver,this.fiRecorded=!1,"PerformanceObserver"in window&&"function"==typeof window.PerformanceObserver){this.performanceObserver=new PerformanceObserver((function(){return r.perfObserver(...arguments)}));try{this.performanceObserver.observe({entryTypes:["paint"]})}catch(e){}this.lcpPerformanceObserver=new PerformanceObserver((function(){return r.lcpObserver(...arguments)}));try{this.lcpPerformanceObserver.observe({entryTypes:["largest-contentful-paint"]})}catch(e){}this.clsPerformanceObserver=new PerformanceObserver((function(){return r.clsObserver(...arguments)}));try{this.clsPerformanceObserver.observe({type:"layout-shift",buffered:!0})}catch(e){}}this.fiRecorded=!1;["click","keydown","mousedown","pointerdown","touchstart"].forEach((e=>{(0,c.iz)(e,(function(){return r.captureInteraction(...arguments)}))})),(0,s.N)((()=>{this.pageHiddenTime=(0,u.zO)(),(0,a.p)("docHidden",[this.pageHiddenTime],void 0,h.D.pageViewTiming,this.ee)}),!0),(0,c.bP)("pagehide",(()=>(0,a.p)("winPagehide",[(0,u.zO)()],void 0,h.D.pageViewTiming,this.ee))),this.importAggregator()}}perfObserver(e,t){e.getEntries().forEach((e=>{"first-paint"===e.name?(0,a.p)("timing",["fp",Math.floor(e.startTime)],void 0,h.D.pageViewTiming,this.ee):"first-contentful-paint"===e.name&&(0,a.p)("timing",["fcp",Math.floor(e.startTime)],void 0,h.D.pageViewTiming,this.ee)}))}lcpObserver(e,t){var r=e.getEntries();if(r.length>0){var n=r[r.length-1];if(this.pageHiddenTime<n.startTime)return;var i=[n],o=this.addConnectionAttributes({});o&&i.push(o),(0,a.p)("lcp",i,void 0,h.D.pageViewTiming,this.ee)}}clsObserver(e){e.getEntries().forEach((e=>{e.hadRecentInput||(0,a.p)("cls",[e],void 0,h.D.pageViewTiming,this.ee)}))}addConnectionAttributes(e){var t=navigator.connection||navigator.mozConnection||navigator.webkitConnection;if(t)return t.type&&(e["net-type"]=t.type),t.effectiveType&&(e["net-etype"]=t.effectiveType),t.rtt&&(e["net-rtt"]=t.rtt),t.downlink&&(e["net-dlink"]=t.downlink),e}captureInteraction(e){if(e instanceof d.Yu.EV&&!this.fiRecorded){var t=Math.round(e.timeStamp),r={type:e.type};this.addConnectionAttributes(r),t<=(0,u.zO)()?r.fid=(0,u.zO)()-t:t>(0,u.os)()&&t<=Date.now()?(t-=(0,u.os)(),r.fid=(0,u.zO)()-t):t=(0,u.zO)(),this.fiRecorded=!0,(0,a.p)("timing",["fi",t,r],void 0,h.D.pageViewTiming,this.ee)}}}n=g,i="featureName",o=l.t,(i=function(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}(i))in n?Object.defineProperty(n,i,{value:o,enumerable:!0,configurable:!0,writable:!0}):n[i]=o},2628:(e,t,r)=>{"use strict";r.r(t),r.d(t,{ADD_EVENT_LISTENER:()=>g,BST_RESOURCE:()=>a,BST_TIMER:()=>l,END:()=>u,FEATURE_NAME:()=>i,FN_END:()=>f,FN_START:()=>d,ORIG_EVENT:()=>p,PUSH_STATE:()=>h,RESOURCE:()=>s,RESOURCE_TIMING_BUFFER_FULL:()=>o,START:()=>c});var n=r(6562);const i=r(2325).D.sessionTrace,o="resourcetimingbufferfull",a="bstResource",s="resource",c="-start",u="-end",d="fn"+c,f="fn"+u,l="bstTimer",h="pushState",p=n.Yu.EV,g="addEventListener"},6649:(e,t,r)=>{"use strict";r.r(t),r.d(t,{Instrument:()=>j});var n=r(9252),i=r(7264),o=r(6408),a=r(8544),s=r(2053),c=r(6114),u=r(2628),d=r(2325),f=r(2374);function l(e,t){!function(e,t){if(t.has(e))throw new TypeError("Cannot initialize the same private elements twice on an object")}(e,t),t.add(e)}const{BST_RESOURCE:h,BST_TIMER:p,END:g,FEATURE_NAME:v,FN_END:m,FN_START:b,ADD_EVENT_LISTENER:y,PUSH_STATE:w,RESOURCE:E,RESOURCE_TIMING_BUFFER_FULL:A,START:x,ORIG_EVENT:O}=u,T="clearResourceTimings";var S,_,I,P=new WeakSet;class j extends c.S{constructor(e,t){if(super(e,t,v,!(arguments.length>2&&void 0!==arguments[2])||arguments[2]),l(this,P),!f.il)return;const r=this.ee;this.timerEE=(0,i.BV)(r),this.rafEE=(0,i.gy)(r),(0,i.QU)(r),(0,i.em)(r),r.on(b,(function(e,t){e[0]instanceof O&&(this.bstStart=(0,s.zO)())})),r.on(m,(function(e,t){var i=e[0];i instanceof O&&(0,n.p)("bst",[i,t,this.bstStart,(0,s.zO)()],void 0,d.D.sessionTrace,r)})),this.timerEE.on(b,(function(e,t,r){this.bstStart=(0,s.zO)(),this.bstType=r})),this.timerEE.on(m,(function(e,t){(0,n.p)(p,[t,this.bstStart,(0,s.zO)(),this.bstType],void 0,d.D.sessionTrace,r)})),this.rafEE.on(b,(function(){this.bstStart=(0,s.zO)()})),this.rafEE.on(m,(function(e,t){(0,n.p)(p,[t,this.bstStart,(0,s.zO)(),"requestAnimationFrame"],void 0,d.D.sessionTrace,r)})),r.on(w+x,(function(e){this.time=(0,s.zO)(),this.startPath=location.pathname+location.hash})),r.on(w+g,(function(e){(0,n.p)("bstHist",[location.pathname+location.hash,this.startPath,this.time],void 0,d.D.sessionTrace,r)})),(0,o.W)()?((0,n.p)(h,[window.performance.getEntriesByType("resource")],void 0,d.D.sessionTrace,r),function(){var e=new PerformanceObserver(((e,t)=>{var i=e.getEntries();(0,n.p)(h,[i],void 0,d.D.sessionTrace,r)}));try{e.observe({entryTypes:["resource"]})}catch(e){}}()):window.performance[T]&&window.performance[y]&&window.performance.addEventListener(A,this.onResourceTimingBufferFull,(0,a.m$)(!1)),document.addEventListener("scroll",this.noOp,(0,a.m$)(!1)),document.addEventListener("keypress",this.noOp,(0,a.m$)(!1)),document.addEventListener("click",this.noOp,(0,a.m$)(!1)),this.abortHandler=function(e,t,r){if(!t.has(e))throw new TypeError("attempted to get private field on non-instance");return r}(this,P,R),this.importAggregator()}noOp(e){}onResourceTimingBufferFull(e){if((0,n.p)(h,[window.performance.getEntriesByType(E)],void 0,d.D.sessionTrace,this.ee),window.performance[T])try{window.performance.removeEventListener(A,this.onResourceTimingBufferFull,!1)}catch(e){}}}function R(){window.performance.removeEventListener(A,this.onResourceTimingBufferFull,!1),(0,i.Zw)(this.ee),(0,i.XV)(this.ee),(0,i.lx)(this.ee),(0,i.hF)(this.ee),this.abortHandler=void 0}S=j,I=v,(_=function(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!=typeof n)return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}(_="featureName"))in S?Object.defineProperty(S,_,{value:I,enumerable:!0,configurable:!0,writable:!0}):S[_]=I},1509:(e,t,r)=>{"use strict";r.d(t,{W:()=>s});var n=r(6562),i=r(3752),o=r(2384),a=r(6797);class s{constructor(e,t,r){this.agentIdentifier=e,this.aggregator=t,this.ee=i.ee.get(e,(0,n.OP)(this.agentIdentifier).isolatedBacklog),this.featureName=r,this.blocked=!1,this.checkConfiguration()}checkConfiguration(){if(!(0,n.lF)(this.agentIdentifier)){let e={...(0,a.gG)().info?.jsAttributes};try{e={...e,...(0,n.C5)(this.agentIdentifier)?.jsAttributes}}catch(e){}(0,o.j)(this.agentIdentifier,{...(0,a.gG)(),info:{...(0,a.gG)().info,jsAttributes:e}})}}}},6114:(e,t,r)=>{"use strict";r.d(t,{S:()=>c});var n=r(4329),i=r(1509),o=r(2650),a=r(2374),s=r(8610);class c extends i.W{constructor(e,t,r){let i=!(arguments.length>3&&void 0!==arguments[3])||arguments[3];super(e,t,r),this.hasAggregator=!1,this.auto=i,this.abortHandler,i&&(0,n.R)(e,r)}importAggregator(){if(this.hasAggregator||!this.auto)return;this.hasAggregator=!0;const e=async()=>{try{const{lazyLoader:e}=await r.e(729).then(r.bind(r,8110)),{Aggregate:t}=await e(this.featureName,"aggregate");new t(this.agentIdentifier,this.aggregator)}catch(e){(0,s.Z)("Downloading ".concat(this.featureName," failed...")),this.abortHandler?.()}};a.v6?e():(0,o.b)((()=>e()),!0)}}},2384:(e,t,r)=>{"use strict";r.d(t,{j:()=>y});var n=r(8683),i=r.n(n),o=r(2325),a=r(6562),s=r(9252),c=r(7022),u=r(3752),d=r(2053),f=r(4329),l=r(2650),h=r(2374),p=r(8610);function g(e){["setErrorHandler","finished","addToTrace","inlineHit","addRelease","addPageAction","setCurrentRouteName","setPageViewName","setCustomAttribute","interaction","noticeError"].forEach((t=>{e[t]=function(){for(var r=arguments.length,n=new Array(r),i=0;i<r;i++)n[i]=arguments[i];return function(t){for(var r=arguments.length,n=new Array(r>1?r-1:0),i=1;i<r;i++)n[i-1]=arguments[i];Object.values(e.initializedAgents).forEach((e=>{e.exposed&&e.api[t]&&e.api[t](...n)}))}(t,...n)}}))}var v=r(6797);const m={stn:o.D.sessionTrace,err:o.D.jserrors,ins:o.D.pageAction,spa:o.D.spa};const b={};function y(e){let t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},n=arguments.length>2?arguments[2]:void 0,y=arguments.length>3?arguments[3]:void 0,{init:w,info:E,loader_config:A,runtime:x={loaderType:n},exposed:O=!0}=t;const T=(0,v.gG)();let S={};return E||(w=T.init,E=T.info,A=T.loader_config,S=T),h.v6&&(E.jsAttributes={...E.jsAttributes,isWorker:!0}),(0,a.CX)(e,E),(0,a.Dg)(e,w||{}),(0,a.GE)(e,A||{}),(0,a.sU)(e,x),function(e,t,n){n||(0,f.R)(e,"api"),g(t);var v=u.ee.get(e),m=v.get("tracer"),b="api-",y=b+"ixn-";function w(){}(0,c.D)(["setErrorHandler","finished","addToTrace","inlineHit","addRelease"],(function(e,r){t[r]=A(b,r,!0,"api")})),t.addPageAction=A(b,"addPageAction",!0,o.D.pageAction),t.setCurrentRouteName=A(b,"routeName",!0,o.D.spa),t.setPageViewName=function(t,r){if("string"==typeof t)return"/"!==t.charAt(0)&&(t="/"+t),(0,a.OP)(e).customTransaction=(r||"http://custom.transaction")+t,A(b,"setPageViewName",!0,"api")()},t.setCustomAttribute=function(t,r){const n=(0,a.C5)(e);return(0,a.CX)(e,{...n,jsAttributes:{...n.jsAttributes,[t]:r}}),A(b,"setCustomAttribute",!0,"api")()},t.interaction=function(){return(new w).get()};var E=w.prototype={createTracer:function(e,t){var r={},n=this,i="function"==typeof t;return(0,s.p)(y+"tracer",[(0,d.zO)(),e,r],n,o.D.spa,v),function(){if(m.emit((i?"":"no-")+"fn-start",[(0,d.zO)(),n,i],r),i)try{return t.apply(this,arguments)}catch(e){throw m.emit("fn-err",[arguments,this,"string"==typeof e?new Error(e):e],r),e}finally{m.emit("fn-end",[(0,d.zO)()],r)}}}};function A(e,t,r,n){return function(){return(0,s.p)("record-supportability",["API/"+t+"/called"],void 0,o.D.metrics,v),(0,s.p)(e+t,[(0,d.zO)()].concat(i()(arguments)),r?null:this,n,v),r?void 0:this}}function x(){r.e(439).then(r.bind(r,5692)).then((t=>{let{setAPI:r}=t;r(e),(0,f.L)(e,"api")})).catch((()=>(0,p.Z)("Downloading runtime APIs failed...")))}(0,c.D)("actionText,setName,setAttribute,save,ignore,onEnd,getContext,end,get".split(","),(function(e,t){E[t]=A(y,t,void 0,o.D.spa)})),t.noticeError=function(e,t){"string"==typeof e&&(e=new Error(e)),(0,s.p)("record-supportability",["API/noticeError/called"],void 0,o.D.metrics,v),(0,s.p)("err",[e,(0,d.zO)(),!1,t],void 0,o.D.jserrors,v)},h.v6?x():(0,l.b)((()=>x()),!0)}(e,S,y),(0,v.Qy)(e,T,"api"),(0,v.Qy)(e,O,"exposed"),h.v6||((0,v.EZ)("activatedFeatures",b),(0,v.EZ)("setToken",(t=>function(e,t){var r=u.ee.get(t);e&&"object"==typeof e&&((0,c.D)(e,(function(e,t){if(!t)return(0,s.p)("block-"+e,[],void 0,m[e],r);t&&!b[e]&&((0,s.p)("feat-"+e,[],void 0,m[e],r),b[e]=!0)})),(0,f.L)(t,o.D.pageViewEvent))}(t,e)))),S}},909:(e,t,r)=>{"use strict";r.d(t,{Z:()=>i,q:()=>o});var n=r(2325);function i(e){switch(e){case n.D.ajax:return[n.D.jserrors];case n.D.sessionTrace:return[n.D.ajax,n.D.pageViewEvent];case n.D.pageViewTiming:return[n.D.pageViewEvent];default:return[]}}function o(e){return e===n.D.jserrors?[]:["auto"]}},2325:(e,t,r)=>{"use strict";r.d(t,{D:()=>n,p:()=>i});const n={ajax:"ajax",jserrors:"jserrors",metrics:"metrics",pageAction:"page_action",pageViewEvent:"page_view_event",pageViewTiming:"page_view_timing",sessionTrace:"session_trace",spa:"spa"},i={[n.pageViewEvent]:1,[n.pageViewTiming]:2,[n.metrics]:3,[n.jserrors]:4,[n.ajax]:5,[n.sessionTrace]:6,[n.pageAction]:7,[n.spa]:8}},8683:e=>{e.exports=function(e,t,r){t||(t=0),void 0===r&&(r=e?e.length:0);for(var n=-1,i=r-t||0,o=Array(i<0?0:i);++n<i;)o[n]=e[t+n];return o}}},n={};function i(e){var t=n[e];if(void 0!==t)return t.exports;var o=n[e]={exports:{}};return r[e](o,o.exports,i),o.exports}i.m=r,i.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return i.d(t,{a:t}),t},i.d=(e,t)=>{for(var r in t)i.o(t,r)&&!i.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},i.f={},i.e=e=>Promise.all(Object.keys(i.f).reduce(((t,r)=>(i.f[r](e,t),t)),[])),i.u=e=>(({78:"page_action-aggregate",147:"metrics-aggregate",193:"session_trace-aggregate",225:"ajax-instrument",317:"jserrors-aggregate",348:"page_view_timing-aggregate",439:"async-api",578:"jserrors-instrument",729:"lazy-loader",757:"session_trace-instrument",786:"page_view_event-aggregate",873:"spa-aggregate",876:"spa-instrument",898:"ajax-aggregate",908:"page_action-instrument"}[e]||e)+"."+{78:"92657d87",118:"d37755e4",147:"b4a54ed9",193:"94c80cda",225:"1e8aaf7f",264:"bcaf68fc",317:"ef250e1c",348:"e791ce32",439:"6bb277af",578:"1eaebfa5",729:"48127245",757:"64f1d623",786:"29613e65",873:"6bec5056",876:"f3685aa9",898:"fc672923",908:"64360627"}[e]+"-1225.min.js"),i.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),e={},t="NRBA:",i.l=(r,n,o,a)=>{if(e[r])e[r].push(n);else{var s,c;if(void 0!==o)for(var u=document.getElementsByTagName("script"),d=0;d<u.length;d++){var f=u[d];if(f.getAttribute("src")==r||f.getAttribute("data-webpack")==t+o){s=f;break}}s||(c=!0,(s=document.createElement("script")).charset="utf-8",s.timeout=120,i.nc&&s.setAttribute("nonce",i.nc),s.setAttribute("data-webpack",t+o),s.src=r),e[r]=[n];var l=(t,n)=>{s.onerror=s.onload=null,clearTimeout(h);var i=e[r];if(delete e[r],s.parentNode&&s.parentNode.removeChild(s),i&&i.forEach((e=>e(n))),t)return t(n)},h=setTimeout(l.bind(null,void 0,{type:"timeout",target:s}),12e4);s.onerror=l.bind(null,s.onerror),s.onload=l.bind(null,s.onload),c&&document.head.appendChild(s)}},i.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.p="https://js-agent.newrelic.com/",(()=>{var e={137:0,308:0,225:0,578:0,908:0,757:0,264:0};i.f.j=(t,r)=>{var n=i.o(e,t)?e[t]:void 0;if(0!==n)if(n)r.push(n[2]);else{var o=new Promise(((r,i)=>n=e[t]=[r,i]));r.push(n[2]=o);var a=i.p+i.u(t),s=new Error;i.l(a,(r=>{if(i.o(e,t)&&(0!==(n=e[t])&&(e[t]=void 0),n)){var o=r&&("load"===r.type?"missing":r.type),a=r&&r.target&&r.target.src;s.message="Loading chunk "+t+" failed.\n("+o+": "+a+")",s.name="ChunkLoadError",s.type=o,s.request=a,n[1](s)}}),"chunk-"+t,t)}};var t=(t,r)=>{var n,o,[a,s,c]=r,u=0;if(a.some((t=>0!==e[t]))){for(n in s)i.o(s,n)&&(i.m[n]=s[n]);if(c)c(i)}for(t&&t(r);u<a.length;u++)o=a[u],i.o(e,o)&&e[o]&&e[o][0](),e[o]=0},r=window.webpackChunkNRBA=window.webpackChunkNRBA||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})();var o={};(()=>{"use strict";i.r(o);var e=i(2325),t=i(6562);const r=Object.values(e.D);function n(e){const n={};return r.forEach((r=>{n[r]=function(e,r){return!1!==(0,t.Mt)(r,"".concat(e,".enabled"))}(r,e)})),n}var a=i(2384),s=i(909),c=i(9557),u=i(7022);class d extends c.w{constructor(e){super(e),this.aggregatedData={}}store(e,t,r,n,i){var o=this.getBucket(e,t,r,i);return o.metrics=function(e,t){t||(t={count:0});return t.count+=1,(0,u.D)(e,(function(e,r){t[e]=f(r,t[e])})),t}(n,o.metrics),o}merge(e,t,r,n,i){var o=this.getBucket(e,t,n,i);if(o.metrics){var a=o.metrics;a.count+=r.count,(0,u.D)(r,(function(e,t){if("count"!==e){var n=a[e],i=r[e];i&&!i.c?a[e]=f(i.t,n):a[e]=function(e,t){if(!t)return e;t.c||(t=l(t.t));return t.min=Math.min(e.min,t.min),t.max=Math.max(e.max,t.max),t.t+=e.t,t.sos+=e.sos,t.c+=e.c,t}(i,a[e])}}))}else o.metrics=r}storeMetric(e,t,r,n){var i=this.getBucket(e,t,r);return i.stats=f(n,i.stats),i}getBucket(e,t,r,n){this.aggregatedData[e]||(this.aggregatedData[e]={});var i=this.aggregatedData[e][t];return i||(i=this.aggregatedData[e][t]={params:r||{}},n&&(i.custom=n)),i}get(e,t){return t?this.aggregatedData[e]&&this.aggregatedData[e][t]:this.aggregatedData[e]}take(e){for(var t={},r="",n=!1,i=0;i<e.length;i++)t[r=e[i]]=h(this.aggregatedData[r]),t[r].length&&(n=!0),delete this.aggregatedData[r];return n?t:null}}function f(e,t){return null==e?function(e){e?e.c++:e={c:1};return e}(t):t?(t.c||(t=l(t.t)),t.c+=1,t.t+=e,t.sos+=e*e,e>t.max&&(t.max=e),e<t.min&&(t.min=e),t):{t:e}}function l(e){return{t:e,min:e,max:e,sos:e*e,c:1}}function h(e){return"object"!=typeof e?[]:(0,u.D)(e,p)}function p(e,t){return t}var g=i(6797),v=i(5526),m=i(8610);var b=i(5637),y=i(7817),w=i(600),E=i(9715),A=i(948),x=i(6649),O=i(488);new class{constructor(t){let r=arguments.length>1&&void 0!==arguments[1]?arguments[1]:(0,v.ky)(16);this.agentIdentifier=r,this.sharedAggregator=new d({agentIdentifier:this.agentIdentifier}),this.features={},this.desiredFeatures=t.features||[],this.desiredFeatures.sort(((t,r)=>e.p[t.featureName]-e.p[r.featureName])),Object.assign(this,(0,a.j)(this.agentIdentifier,t,t.loaderType||"agent")),this.start()}get config(){return{info:(0,t.C5)(this.agentIdentifier),init:(0,t.P_)(this.agentIdentifier),loader_config:(0,t.DL)(this.agentIdentifier),runtime:(0,t.OP)(this.agentIdentifier)}}start(){const e="features";try{const t=n(this.agentIdentifier);this.desiredFeatures.forEach((e=>{if(t[e.featureName]){const r=(0,s.Z)(e.featureName);r.every((e=>t[e]))||(0,m.Z)("".concat(e.featureName," is enabled but one or more dependent features has been disabled (").concat(JSON.stringify(r),"). This may cause unintended consequences or missing data...")),this.features[e.featureName]=new e(this.agentIdentifier,this.sharedAggregator)}})),(0,g.Qy)(this.agentIdentifier,this.features,e)}catch(t){(0,m.Z)("Failed to initialize all enabled instrument classes (agent aborted) -",t);for(const e in this.features)this.features[e].abortHandler?.();const r=(0,g.fP)();return delete r.initializedAgents[this.agentIdentifier]?.api,delete r.initializedAgents[this.agentIdentifier]?.[e],delete this.sharedAggregator,delete r.ee?.get(this.agentIdentifier),!1}}}({features:[b.Instrument,y.Instrument,x.Instrument,A.Instrument,w.Instrument,O.Instrument,E.Instrument],loaderType:"pro"})})(),window.NRBA=o})();</script><script type="text/javascript">window.NREUM||(NREUM={});NREUM.info={"beacon":"bam.nr-data.net","errorBeacon":"bam.nr-data.net","licenseKey":"0ed0ce50b0","applicationID":"5588594","transactionName":"Y1BRbUUFWkMEWxYMV1oadUxZB0BZClZNCV5ZG0RcVUpDRxIWAxVIRxteTEQNVx4TUQcSSxpWUk1WCFtXEF1YMUpVVlhtVgNHHgJdFg==","queueTime":0,"applicationTime":616,"agent":""}</script>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title aria-live="assertive">Tags - Naughty Girl — Beyoncé | Last.fm</title>
<link data-replaceable-head-tag="" href="https://www.last.fm/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" rel="canonical"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="en" rel="alternate"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/de/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="de" rel="alternate"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/es/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="es" rel="alternate"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/fr/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="fr" rel="alternate"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/it/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="it" rel="alternate"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/ja/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="ja" rel="alternate"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/pl/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="pl" rel="alternate"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/pt/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="pt" rel="alternate"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/ru/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="ru" rel="alternate"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/sv/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="sv" rel="alternate"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/tr/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="tr" rel="alternate"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/zh/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="zh" rel="alternate"/>
<link data-replaceable-head-tag="" href="https://www.last.fm/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" hreflang="x-default" rel="alternate"/>
<meta content="Read about Naughty Girl by Beyoncé and see the artwork, lyrics and similar artists." data-replaceable-head-tag="" name="description"/>
<meta content="Tags - Naughty Girl — Beyoncé | Last.fm" data-replaceable-head-tag="" property="og:title"/>
<meta content="Read about Naughty Girl by Beyoncé and see the artwork, lyrics and similar artists." data-replaceable-head-tag="" property="og:description"/>
<meta content="website" data-replaceable-head-tag="" property="og:type"/>
<meta content="Last.fm" data-replaceable-head-tag="" property="og:site_name"/>
<meta content="https://www.last.fm/music/Beyonc%C3%A9/_/Naughty+Girl/+tags" data-replaceable-head-tag="" property="og:url">
<meta content="https://lastfm.freetls.fastly.net/i/u/ar0/4128a6eb29f94943c9d206c08e625904.jpg" data-replaceable-head-tag="" property="og:image"/>
<meta content="1200" data-replaceable-head-tag="" property="og:image:width"/>
<meta content="630" data-replaceable-head-tag="" property="og:image:height"/>
<meta content="Tags - Naughty Girl — Beyoncé | Last.fm" data-replaceable-head-tag="" name="twitter:title"/>
<meta content="Read about Naughty Girl by Beyoncé and see the artwork, lyrics and similar artists." data-replaceable-head-tag="" name="twitter:description"/>
<meta content="https://lastfm.freetls.fastly.net/i/u/ar0/4128a6eb29f94943c9d206c08e625904.jpg" data-replaceable-head-tag="" name="twitter:image"/>
<meta content="summary" data-replaceable-head-tag="" name="twitter:card"/>
<meta content="@lastfm" data-replaceable-head-tag="" name="twitter:site"/>
<link href="https://www.last.fm/static/images/lastfm_avatar_applemusic.b06eb8ad89be.png" rel="apple-music-app-icon"/>
<link href="https://www.last.fm/static/images/lastfm_avatar_applemusic.b06eb8ad89be.png" rel="apple-touch-icon-precomposed"/>
<link href="https://www.last.fm/static/images/lastfm_avatar_applemusic.b06eb8ad89be.png" rel="apple-touch-icon"/>
<script>(function(e) { e.className = e.className.replace(/\bno-js\b/,'js'); })(document.documentElement)</script>
<div data-require="tracking/tealium-utag-set" data-tealium-data='{"siteSection": "music", "pageType": "music_track_tags_overview", "pageName": "music/track/tags/overview", "nativeEventTracking": true, "userState": "not authenticated", "userType": "anon", "musicSongTitle": "Naughty Girl", "musicArtistName": "Beyonc\u00e9", "artist": "beyonc\u00e9", "ar": "beyonc\u00e9", "tag": "rnb,sexy,pop,beyonce,femalevocalists,hip-hop"}' data-tealium-environment="prod" id="initial-tealium-data"></div>
<link href="/static/images/favicon.702b239b6194.ico" rel="icon"/>
<link charset="utf-8" data-stylesheet-name="defaults" href="/static/styles/build/anhv2-defaults-c317032780.c31703278066.css" rel="stylesheet"/>
<link charset="utf-8" data-stylesheet-name="app" href="/static/styles/build/app-reduced-257d7cbc62.9e7e5c4afde8.css" rel="stylesheet"/>
<link charset="utf-8" data-stylesheet-name="page-specific" href="/static/styles/build/track-subpage-02516bae26.4be5411aed62.css" rel="stylesheet"/>
<script data-domain-script="d9f750da-0271-4142-9b0e-43d9a3b334d1" src="https://cdn.cookielaw.org/scripttemplates/otSDKStub.js"></script>
<script async="" data-main="/static/js-build/init.ae6f82ee8be5" src="/static/js-build/lib/require/require.0c0e3310c2c2.js"></script>
<!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
<!--[if lt IE 9]>
          <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
          <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
        <![endif]-->
</meta></head>
<body class="catalogue-subpage anhv2 namespace--music_track_tags_overview" data-cbsi-player-config="/static/config/video-player.015786d691c2.xml" data-country-code="FR" data-facebook-placement-id="195612451022080_220502155199776" data-google-maps-api-key="AIzaSyBX6-IE3lz4PpJUSBVIo_dPb0BAyMgi-VE" data-onetrust-prod="" data-partial-refresh-supported="true" data-player-supported="true" data-require="ads/page-ads,ads/searchlinks,player/playlink-handler,dev/grid-overlay,dev/toggle-version,dev/debug-log,dev/debug-image-analysis,dev/js-log,dev/ads-toggle,components/link-block,components/ajax-form,core/media-size-events-v2" data-sensitive-path-regex="^/(../)?(googlec3ea1b252774e1ab\.html|account_deleted|inbox|join|login|lostpassword(/confirm)?|staff|subscribe|support(?!/images|/shouts|/shout)|settings/(account|website|subscription|password|lostpassword)|user/.+?/support)(/.*)?/?$">
<div data-loading-indicator-copy="Loading…" data-require="components/loading-indicator"></div>
<div data-require="components/open-modal,components/submit-to-modal,components/show-alert" data-show-alert-ok-copy="Okay"></div>
<div class="intromercial lastfm-ad-mobile" data-ad="intromercial" data-ads-placement='{"id": "intromercial", "is_mobile_and_desktop": true, "out_of_page": true, "is_mobile": true}' id="intromercial" style="display: block;">
</div>
<div class="top-bar">
<section aria-disabled="true" aria-label="audio player" class="player-bar inactive" data-player-error-cannot-play-item="Cannot play that item." data-player-error-track-unavailable="Track unavailable." data-player-modal-title="Play video" data-player-status-ad-playing="Ad playing" data-player-status-inactive=" " data-player-status-loading-spotify="Connecting Spotify…" data-player-status-spotify-auth-error="Could not authenticate with Spotify." data-require="player/controls,player/status,player/tracking">
<div class="player-bar-inner-wrap">
<a class="player-bar-artwork js-artwork">
<img alt="" class="" loading="lazy" src="/static/images/defaults/player_default_album.430223706b14.png"/>
</a>
<span class="player-bar-source player-bar-source--spotify">Playing via Spotify</span>
<span class="player-bar-source player-bar-source--youtube">Playing via YouTube</span>
<div class="source-info">
<button aria-controls="player-bar-playback-options" class="player-bar-playback-options-button" data-disclose-hover="">
                    Playback options
                </button>
<div class="player-bar-playback-options-wrap disclose-hide" id="player-bar-playback-options">
<ul class="dropdown-menu-dark player-bar-playback-options-spotify">
<li class="dropdown-menu-non-interactive-item-dark">
<span class="player-bar-listening-on-heading">Listening on…</span>
<span class="player-bar-listening-on js-player-bar-listening-on"></span>
</li>
<li><button class="dropdown-menu-item-dark js-switch-device player-bar-playback-options-switch-device">Switch Spotify device</button></li>
<li><a class="js-source dropdown-menu-item-dark player-bar-playback-options-external-link" target="_blank">Open in Spotify Web Player</a></li>
<li class="menu-separator--dark">
<a class="dropdown-menu-item-dark player-bar-playback-options-settings" href="/login?next=/settings/website">
            Change playback source
        </a>
</li>
</ul>
<ul class="dropdown-menu-dark player-bar-playback-options-youtube">
<li><a class="dropdown-menu-item-dark js-source player-bar-playback-options-external-link" target="_blank">Open on YouTube website</a></li>
<li class="menu-separator--dark">
<a class="dropdown-menu-item-dark player-bar-playback-options-settings" href="/login?next=/settings/website">
            Change playback source
        </a>
</li>
</ul>
</div>
</div>
<div class="player-bar-controls">
<ul aria-label="controls" class="media-controls">
<li>
<button class="js-previous player-bar-btn player-bar-btn--previous" data-analytics-action="PlaybarBackTrack" disabled="">
                            Previous
                        </button>
</li>
<li>
<button class="js-play-pause player-bar-btn player-bar-btn--play" data-analytics-action="PlaybarResumeTrack" data-analytics-action-pause="PlaybarPauseTrack" data-string-pause="Pause" disabled="">
                            Play
                        </button>
</li>
<li>
<button class="js-next player-bar-btn player-bar-btn--next" data-analytics-action="PlaybarSkipTrack" disabled="">
                            Next
                        </button>
</li>
</ul>
<a class="player-bar-skiplink player-bar-skiplink--youtube" href="#youtube-video">Skip to YouTube video</a>
</div>
<div class="player-bar-now-playing">
<div class="player-bar-now-playing-inner-wrap">
<p aria-atomic="true" aria-label="now playing" aria-live="polite" class="player-bar-track js-player-status">
                        Loading player…
                    </p>
<p class="player-bar-error js-player-error player-bar-status--hide">
<span class="player-bar-error-message js-player-error-message"></span>
</p>
</div>
</div>
</div>
<div class="player-bar-progress-wrap">
<div aria-label="progress" class="player-bar-progress" role="timer">
<div class="js-progress-slug player-bar-progress-slug">
<span aria-label="remaining" class="js-progress-remaining player-bar-progress-remaining"></span>
</div>
</div>
</div>
<div data-require="player/scrobble-client"></div>
</section>
<div class="masthead-popup masthead-popup--spotify-scrobbling masthead-popup--hidden" data-require="components/spotify-scrobbling-prompt,components/alert-dismissable,components/spotify-scrobbling-banner" data-spotify-scobbling-fail-modal="/socialmodal/spotify-scrobbling-fail" data-spotify-scobbling-success-modal="/socialmodal/spotify-scrobbling-success">
<div class="masthead-popup-inner">
<h3>Scrobble from Spotify?</h3>
<p>Connect your Spotify account to your Last.fm account and scrobble everything you listen to, from any Spotify app on any device or platform.</p>
<p>
<a class="btn-primary js-setup-spotify-scrobbling" href="/settings/applications">
                    Connect to Spotify
                </a>
</p>
<a class="masthead-popup-close js-alert-dismissable-close" data-close-ajax="" href="/nagbar/dismiss/spotify-scrobbling-prompt?period=permanent">
                Dismiss
            </a>
</div>
</div>
</div>
<div aria-live="polite" class="main-content" id="content" role="main">
<div class="hidden" data-tealium-data='{"siteSection": "music", "pageType": "music_track_tags_overview", "pageName": "music/track/tags/overview", "nativeEventTracking": true, "userState": "not authenticated", "userType": "anon", "musicSongTitle": "Naughty Girl", "musicArtistName": "Beyonc\u00e9", "artist": "beyonc\u00e9", "ar": "beyonc\u00e9", "tag": "rnb,sexy,pop,beyonce,femalevocalists,hip-hop"}' hidden="" id="tlmdata">
</div>
<div data-page-resource-artist-name="Beyoncé" data-page-resource-blacklist-level="" data-page-resource-name="Naughty Girl" data-page-resource-type="track">
<div data-require="components/disclose-base,components/disclose-autoclose-v2,components/disclose-dropdown-v2,components/disclose-dropdown-location-picker-v2,components/disclose-collapsing-nav-v2,components/disclose-artwork,components/disclose-remove,components/disclose-search,components/disclose-hover-v3,components/disclose-select,components/disclose-lazy-buylinks,components/focus-controls,components/prevent-resubmit-v2,components/edit-scrobble,components/toggle-buttons,components/click-proxy,components/bookmark-notification,components/follow-notification,components/tourguide"></div>
<nav class="masthead"><div class="masthead-inner-wrap"><div class="masthead-logo"><span class="masthead-logo-loading"></span><a href="/"> Last.fm</a></div><a aria-controls="masthead-search" class="masthead-search-toggle" data-disclose-search="" href="/search">Search</a><form action="/search" class="masthead-search-form disclose-hide disclose-hide--js-only" id="masthead-search" method="get"><div class="masthead-search-inner-wrap"><label class="sr-only" for="masthead-search-field">Search</label><input class="masthead-search-field" id="masthead-search-field" name="q" placeholder="Search for music…" type="text"/><button class="masthead-search-submit" type="submit">Search</button></div></form><div class="visible-xs"><button aria-controls="masthead-nav" class="masthead-hamburger-toggle" data-disclose-autoclose="">Toggle navigation</button><ul aria-label="Primary navigation" class="masthead-nav disclose-hide disclose-hide--js-only" id="masthead-nav"><li class="masthead-nav-item masthead-nav-pro"><a class="masthead-nav-control masthead-pro-text" data-analytics-action="UserMenuClick" data-analytics-label="subscribe" href="/pro">Upgrade to Pro</a></li><li class="masthead-nav-item"><a class="masthead-nav-control" data-analytics-action="NavigationLink" data-analytics-label="live" href="/dashboard">Live</a></li><li class="masthead-nav-item"><a class="masthead-nav-control masthead-nav-control--active" data-analytics-action="NavigationLink" data-analytics-label="music" href="/music">Music</a></li><li class="masthead-nav-item"><a class="masthead-nav-control" data-analytics-action="NavigationLink" data-analytics-label="charts" href="/charts">Charts</a></li><li class="masthead-nav-item"><a class="masthead-nav-control" data-analytics-action="NavigationLink" data-analytics-label="events" href="/events">Events</a></li><li class="masthead-nav-item"><a class="masthead-nav-control" data-analytics-action="NavigationLink" data-analytics-label="features" href="/features">Features</a></li>
<li class="masthead-nav-item">
<a class="masthead-nav-control" data-analytics-action="UserMenuClick" data-analytics-label="subscribe" href="/pro">Subscribe</a>
</li>
<li class="masthead-nav-item">
<a class="masthead-nav-control" href="/login">Log In</a>
</li>
<li class="masthead-nav-item masthead-nav-join">
<a class="btn-secondary join-cta-button" data-analytics-action="SignUpClick" href="/join">Sign Up</a>
</li>
</ul></div><div class="navlist navlist--more masthead-nav hidden-xs" data-more-string="More…" data-require="components/primary-nav"><ul aria-label="Primary navigation" class="js-navlist-items navlist-items"><li class="masthead-nav-item masthead-nav-pro"><a class="masthead-nav-control masthead-pro-text" data-analytics-action="UserMenuClick" data-analytics-label="subscribe" href="/pro">Upgrade to Pro</a></li><li class="masthead-nav-item"><a class="masthead-nav-control" data-analytics-action="NavigationLink" data-analytics-label="live" href="/dashboard">Live</a></li><li class="masthead-nav-item"><a class="masthead-nav-control masthead-nav-control--active" data-analytics-action="NavigationLink" data-analytics-label="music" href="/music">Music</a></li><li class="masthead-nav-item"><a class="masthead-nav-control" data-analytics-action="NavigationLink" data-analytics-label="charts" href="/charts">Charts</a></li><li class="masthead-nav-item"><a class="masthead-nav-control" data-analytics-action="NavigationLink" data-analytics-label="events" href="/events">Events</a></li><li class="masthead-nav-item"><a class="masthead-nav-control" data-analytics-action="NavigationLink" data-analytics-label="features" href="/features">Features</a></li></ul></div>
<ul class="site-auth site-auth--anon hidden-xs">
<li class="site-auth-item"><a class="site-auth-control" href="/login">Log In</a></li><li class="site-auth-item"><a class="site-auth-control btn-secondary join-cta-button" data-analytics-action="SignUpClick" href="/join">Sign Up</a></li>
</ul>
</div></nav>
<div class="" data-lazy-load-content="/nagbar/language-prompt" data-require="components/language-prompt">
</div>
<div class="nag-bar nag-bar--plybar-masthead-release-warning" role="status">
<div class="container">
<p class="nag-bar-message">

        A new version of Last.fm is available, to keep everything running smoothly, please <a href="javascript:window.location.reload()">reload</a> the site.

            </p>
</div>
</div>
<div data-require="core/redirect-bar" id="redirect-bar">
<script id="redirect-bar-data" type="application/json">
            {
                "content": {
                    "redirect": "Redirected from {link}."
                },

                    "overlayColor": null

            }
        </script>
<redirect-bar></redirect-bar>
</div>
<div class="adaptive-skin-container" id="mantle_skin">
<div class="adaptive-skin-wrapper">
<div class="adaptive-skin-left" id="adSkinLeft"></div>
<div class="adaptive-skin-right" id="adSkinRight"></div>
</div>
<header class="header-new header-new--track header-new--subpage">
<div class="header-new-inner" style="background: #6E3F3B">
<div class="header-new-background">
<div class="header-new-background-image" content="https://lastfm.freetls.fastly.net/i/u/ar0/e085c3b6f6d54a7b5097fa288eaf3890.jpg" itemprop="image" style="background-image: url(https://lastfm.freetls.fastly.net/i/u/ar0/e085c3b6f6d54a7b5097fa288eaf3890.jpg);"></div>
<div class="header-new-background-overlay-mobile" style="
                        background: linear-gradient(
                            rgba(110,63,59,0),
                            rgba(110,63,59,1)
                        );
                    "></div>
<div class="header-new-background-overlay" style="
                        background: linear-gradient(
                            0.25turn,
                            rgba(110,63,59,1),
                            rgba(110,63,59,0)
                        );
                    "></div>
</div>
<div class="header-new-content">
<span itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<a class="header-new-crumb" href="/music/Beyonc%C3%A9" itemprop="url"><span itemprop="name">Beyoncé</span></a>
</span>
<h1 class="header-new-title" itemprop="name">Naughty Girl</h1>
<link href="/music/Beyonc%C3%A9/_/Naughty+Girl" itemprop="url">
<nav aria-label="Secondary navigation" class="navlist secondary-nav navlist--more" data-more-string="More…" data-require="components/collapsing-nav-v2">
<ul class="navlist-items js-navlist-items">
<li class="navlist-item secondary-nav-item secondary-nav-item--overview"><a class="secondary-nav-item-link" href="/music/Beyonc%C3%A9/_/Naughty+Girl">
                            Overview

                        </a></li><li class="navlist-item secondary-nav-item secondary-nav-item--albums"><a class="secondary-nav-item-link" href="/music/Beyonc%C3%A9/_/Naughty+Girl/+albums">
                            Albums

                        </a></li><li class="navlist-item secondary-nav-item secondary-nav-item--wiki"><a class="secondary-nav-item-link" href="/music/Beyonc%C3%A9/_/Naughty+Girl/+wiki">
                            Wiki

                        </a></li><li class="navlist-item secondary-nav-item secondary-nav-item--tags"><a class="secondary-nav-item-link secondary-nav-item-link--active" href="/music/Beyonc%C3%A9/_/Naughty+Girl/+tags">
                            Tags

                                <span class="sr-only">(current section)</span>
</a></li><li class="navlist-item secondary-nav-item secondary-nav-item--shoutbox"><a class="secondary-nav-item-link" href="/music/Beyonc%C3%A9/_/Naughty+Girl/+shoutbox">
                            Shouts

                        </a></li>
</ul>
</nav>
</link></div>
</div>
</header>
<div class="full-bleed-ad-container" data-ad-container="">
<div class="leader_plus_top lastfm-ad" data-ad="leader_plus_top" data-ads-placement='{"id": "leader_plus_top", "sizes": [[728, 90], [970, 66], [970, 250], [728, 91]], "targeting": {"pos": "top"}, "adblock_message": true}' id="leader_plus_top">
</div>
</div>
<div class="container page-content">
<div class="tonefuze tonefuze--mobile visible-xs" data-require="
                ads/tonefuze

            " data-tonefuze-artist="Beyoncé" data-tonefuze-flex="False" data-tonefuze-id="100000055" data-tonefuze-track="Naughty Girl" id="tonefuze-mobile">
</div>
<div class="row buffer-4 buffer-reset@sm">
<div class="col-main">
<section>
<div class="section-controls buffer-4 buffer-reset@sm">
<h2 class="subpage-title">Tags</h2>
<a class="btn-add" data-open-modal="/join/modal?action=tag-track&amp;back_to=%2Fmusic%2FBeyonc%25C3%25A9%2F_%2FNaughty%2BGirl%2F%2Btags%2Fadd" href="/login?next=/music/Beyonc%25C3%25A9/_/Naughty%2BGirl/%2Btags/add">Add Tags</a>
</div>
<ol class="buffer-standard big-tags big-tags--with-6">
<li class="big-tags-item-wrap" itemscope="" itemtype="">
<div class="big-tags-item js-link-block link-block">
<h3 class="big-tags-item-name" itemprop="name">
<a class="link-block-target" href="/tag/rnb" itemprop="url">rnb</a>
</h3>
<p class="big-tags-item-context">

        Including <a href="/music/Rihanna">Rihanna</a>, <a href="/music/Beyonc%C3%A9">Beyoncé</a> and <a href="/music/Alicia+Keys">Alicia Keys</a>
</p>
<div class="media-item">
<span class="overlay-image big-tags-item-image" style="background: rgba(153,108,78,1)">
<img alt="" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/6c2f55ff414a47d8c78d9684dfddd3eb.jpg"/>
</span>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/tag/rnb" tabindex="-1"></a>
</div>
</li>
<li class="big-tags-item-wrap" itemscope="" itemtype="">
<div class="big-tags-item js-link-block link-block">
<h3 class="big-tags-item-name" itemprop="name">
<a class="link-block-target" href="/tag/sexy" itemprop="url">sexy</a>
</h3>
<p class="big-tags-item-context">

        Including <a href="/music/Shakira">Shakira</a>, <a href="/music/Britney+Spears">Britney Spears</a> and <a href="/music/Nicole+Scherzinger">Nicole Scherzinger</a>
</p>
<div class="media-item">
<span class="overlay-image big-tags-item-image" style="background: rgba(4,116,155,1)">
<img alt="" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/85fb31fac28db82cd83d8f7efb628605.jpg"/>
</span>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/tag/sexy" tabindex="-1"></a>
</div>
</li>
<li class="big-tags-item-wrap" itemscope="" itemtype="">
<div class="big-tags-item js-link-block link-block">
<h3 class="big-tags-item-name" itemprop="name">
<a class="link-block-target" href="/tag/pop" itemprop="url">pop</a>
</h3>
<p class="big-tags-item-context">

        Including <a href="/music/Michael+Jackson">Michael Jackson</a>, <a href="/music/Madonna">Madonna</a> and <a href="/music/The+Beatles">The Beatles</a>
</p>
<div class="media-item">
<span class="overlay-image big-tags-item-image" style="background: rgba(127,68,43,1)">
<img alt="" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/ef6fbc2fa8e8184badce0f305b290de4.jpg"/>
</span>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/tag/pop" tabindex="-1"></a>
</div>
</li>
<li class="big-tags-item-wrap" itemscope="" itemtype="">
<div class="big-tags-item js-link-block link-block">
<h3 class="big-tags-item-name" itemprop="name">
<a class="link-block-target" href="/tag/beyonce" itemprop="url">beyonce</a>
</h3>
<p class="big-tags-item-context">

        Including <a href="/music/Beyonc%C3%A9">Beyoncé</a>, <a href="/music/Sevdaliza">Sevdaliza</a> and <a href="/music/Diamanda+Gal%C3%A1s">Diamanda Galás</a>
</p>
<div class="media-item">
<span class="overlay-image big-tags-item-image" style="background: rgba(110,63,59,1)">
<img alt="" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/e085c3b6f6d54a7b5097fa288eaf3890.jpg"/>
</span>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/tag/beyonce" tabindex="-1"></a>
</div>
</li>
<li class="big-tags-item-wrap" itemscope="" itemtype="">
<div class="big-tags-item js-link-block link-block">
<h3 class="big-tags-item-name" itemprop="name">
<a class="link-block-target" href="/tag/female+vocalists" itemprop="url">female vocalists</a>
</h3>
<p class="big-tags-item-context">

        Including <a href="/music/Bj%C3%B6rk">Björk</a>, <a href="/music/Amy+Winehouse">Amy Winehouse</a> and <a href="/music/Tori+Amos">Tori Amos</a>
</p>
<div class="media-item">
<span class="overlay-image big-tags-item-image" style="background: rgba(71,89,101,1)">
<img alt="" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/f244678b6638b7cc8eae528268a3afc7.jpg"/>
</span>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/tag/female+vocalists" tabindex="-1"></a>
</div>
</li>
<li class="big-tags-item-wrap" itemscope="" itemtype="">
<div class="big-tags-item js-link-block link-block">
<h3 class="big-tags-item-name" itemprop="name">
<a class="link-block-target" href="/tag/hip-hop" itemprop="url">hip-hop</a>
</h3>
<p class="big-tags-item-context">

        Including <a href="/music/Eminem">Eminem</a>, <a href="/music/Kanye+West">Kanye West</a> and <a href="/music/Gorillaz">Gorillaz</a>
</p>
<div class="media-item">
<span class="overlay-image big-tags-item-image" style="background: rgba(70,44,39,1)">
<img alt="" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/09898871d5dacd41cc41574b0c053647.jpg"/>
</span>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/tag/hip-hop" tabindex="-1"></a>
</div>
</li>
</ol>
</section>
<section class="buffer-standard section-with-separator visible-xs">
<h3 class="text-18">Similar Tracks</h3>
<ol class="column-tracks column-tracks--with-12">
<li class="column-tracks-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="column-tracks-item js-link-block link-block">
<h3 class="column-tracks-item-name" itemprop="name">
<a class="link-block-target" href="/music/Beyonc%C3%A9/_/Baby+Boy+(feat.+Sean+Paul)" itemprop="url">Baby Boy (feat. Sean Paul)</a>
</h3>
<p class="column-tracks-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Beyonc%C3%A9" itemprop="url">Beyoncé</a>
</span>
</p>
<div class="media-item">
<span class="column-tracks-item-image cover-art">
<img alt="Baby Boy - Single" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/b27d7355750013c04ca5259d44357da3.jpg">
</img></span>
<a class="column-tracks-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Beyoncé" data-artist-url="/music/Beyonc%C3%A9" data-playlink-affiliate="youtube" data-track-name="Baby Boy (feat. Sean Paul)" data-track-url="/music/Beyonc%C3%A9/_/Baby+Boy+(feat.+Sean+Paul)" data-youtube-id="8ucz_pm3LX8" data-youtube-url="https://www.youtube.com/watch?v=8ucz_pm3LX8" href="https://www.youtube.com/watch?v=8ucz_pm3LX8" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Beyonc%C3%A9/_/Baby+Boy+(feat.+Sean+Paul)" tabindex="-1"></a>
</div>
</li>
<li class="column-tracks-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="column-tracks-item js-link-block link-block">
<h3 class="column-tracks-item-name" itemprop="name">
<a class="link-block-target" href="/music/Beyonc%C3%A9/_/Me,+Myself+and+I" itemprop="url">Me, Myself and I</a>
</h3>
<p class="column-tracks-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Beyonc%C3%A9" itemprop="url">Beyoncé</a>
</span>
</p>
<div class="media-item">
<span class="column-tracks-item-image cover-art">
<img alt="Dangerously in Love" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/60978eaf2b29dcee28301eb6fa21a3f5.jpg">
</img></span>
<a class="column-tracks-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Beyoncé" data-artist-url="/music/Beyonc%C3%A9" data-playlink-affiliate="youtube" data-track-name="Me, Myself and I" data-track-url="/music/Beyonc%C3%A9/_/Me,+Myself+and+I" data-youtube-id="4S37SGxZSMc" data-youtube-url="https://www.youtube.com/watch?v=4S37SGxZSMc" href="https://www.youtube.com/watch?v=4S37SGxZSMc" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Beyonc%C3%A9/_/Me,+Myself+and+I" tabindex="-1"></a>
</div>
</li>
<li class="column-tracks-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="column-tracks-item js-link-block link-block">
<h3 class="column-tracks-item-name" itemprop="name">
<a class="link-block-target" href="/music/Destiny%27s+Child/_/Lose+My+Breath" itemprop="url">Lose My Breath</a>
</h3>
<p class="column-tracks-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Destiny%27s+Child" itemprop="url">Destiny's Child</a>
</span>
</p>
<div class="media-item">
<span class="column-tracks-item-image cover-art">
<img alt="Destiny Fulfilled" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/0e3fecb01f78d0ced91432e3a77be2eb.jpg">
</img></span>
<a class="column-tracks-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Destiny's Child" data-artist-url="/music/Destiny%27s+Child" data-playlink-affiliate="youtube" data-track-name="Lose My Breath" data-track-url="/music/Destiny%27s+Child/_/Lose+My+Breath" data-youtube-id="AqeIiF0DlTg" data-youtube-url="https://www.youtube.com/watch?v=AqeIiF0DlTg" href="https://www.youtube.com/watch?v=AqeIiF0DlTg" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Destiny%27s+Child/_/Lose+My+Breath" tabindex="-1"></a>
</div>
</li>
<li class="column-tracks-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="column-tracks-item js-link-block link-block">
<h3 class="column-tracks-item-name" itemprop="name">
<a class="link-block-target" href="/music/Destiny%27s+Child/_/Bootylicious" itemprop="url">Bootylicious</a>
</h3>
<p class="column-tracks-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Destiny%27s+Child" itemprop="url">Destiny's Child</a>
</span>
</p>
<div class="media-item">
<span class="column-tracks-item-image cover-art">
<img alt="Survivor" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/fe3b5b68d86d157e7f55ea341e5a56a4.jpg">
</img></span>
<a class="column-tracks-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Destiny's Child" data-artist-url="/music/Destiny%27s+Child" data-playlink-affiliate="youtube" data-track-name="Bootylicious" data-track-url="/music/Destiny%27s+Child/_/Bootylicious" data-youtube-id="IyYnnUcgeMc" data-youtube-url="https://www.youtube.com/watch?v=IyYnnUcgeMc" href="https://www.youtube.com/watch?v=IyYnnUcgeMc" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Destiny%27s+Child/_/Bootylicious" tabindex="-1"></a>
</div>
</li>
<li class="column-tracks-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="column-tracks-item js-link-block link-block">
<h3 class="column-tracks-item-name" itemprop="name">
<a class="link-block-target" href="/music/Beyonc%C3%A9+&amp;+Shakira/_/Beautiful+Liar" itemprop="url">Beautiful Liar</a>
</h3>
<p class="column-tracks-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Beyonc%C3%A9+&amp;+Shakira" itemprop="url">Beyoncé &amp; Shakira</a>
</span>
</p>
<div class="media-item">
<span class="column-tracks-item-image cover-art">
<img alt="Hit Connection Best Of 2007" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/229e3184a77542f9cc01bd15a3f2658c.jpg">
</img></span>
<a class="column-tracks-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Beyoncé &amp; Shakira" data-artist-url="/music/Beyonc%C3%A9+&amp;+Shakira" data-playlink-affiliate="youtube" data-track-name="Beautiful Liar" data-track-url="/music/Beyonc%C3%A9+&amp;+Shakira/_/Beautiful+Liar" data-youtube-id="QrOe2h9RtWI" data-youtube-url="https://www.youtube.com/watch?v=QrOe2h9RtWI" href="https://www.youtube.com/watch?v=QrOe2h9RtWI" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Beyonc%C3%A9+&amp;+Shakira/_/Beautiful+Liar" tabindex="-1"></a>
</div>
</li>
<li class="column-tracks-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="column-tracks-item js-link-block link-block">
<h3 class="column-tracks-item-name" itemprop="name">
<a class="link-block-target" href="/music/Nicki+Minaj/_/Feeling+Myself" itemprop="url">Feeling Myself</a>
</h3>
<p class="column-tracks-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Nicki+Minaj" itemprop="url">Nicki Minaj</a>
</span>
</p>
<div class="media-item">
<span class="column-tracks-item-image cover-art">
<img alt="The Pinkprint (Deluxe)" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/ae4a60ffc368d5d0081673c9b6d9f91c.jpg">
</img></span>
<a class="column-tracks-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Nicki Minaj" data-artist-url="/music/Nicki+Minaj" data-playlink-affiliate="youtube" data-track-name="Feeling Myself" data-track-url="/music/Nicki+Minaj/_/Feeling+Myself" data-youtube-id="0Kg9xRooTVk" data-youtube-url="https://www.youtube.com/watch?v=0Kg9xRooTVk" href="https://www.youtube.com/watch?v=0Kg9xRooTVk" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Nicki+Minaj/_/Feeling+Myself" tabindex="-1"></a>
</div>
</li>
<li class="column-tracks-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="column-tracks-item js-link-block link-block">
<h3 class="column-tracks-item-name" itemprop="name">
<a class="link-block-target" href="/music/Rihanna/_/Pon+de+Replay" itemprop="url">Pon de Replay</a>
</h3>
<p class="column-tracks-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Rihanna" itemprop="url">Rihanna</a>
</span>
</p>
<div class="media-item">
<span class="column-tracks-item-image cover-art">
<img alt="Music of the Sun" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/41ec6a7494a22ba0a1a99ad5763cc454.jpg"/>
</span>
<a class="column-tracks-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Rihanna" data-artist-url="/music/Rihanna" data-playlink-affiliate="youtube" data-track-name="Pon de Replay" data-track-url="/music/Rihanna/_/Pon+de+Replay" data-youtube-id="oEauWw9ZGrA" data-youtube-url="https://www.youtube.com/watch?v=oEauWw9ZGrA" href="https://www.youtube.com/watch?v=oEauWw9ZGrA" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Rihanna/_/Pon+de+Replay" tabindex="-1"></a>
</div>
</li>
<li class="column-tracks-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="column-tracks-item js-link-block link-block">
<h3 class="column-tracks-item-name" itemprop="name">
<a class="link-block-target" href="/music/Britney+Spears/_/I%27m+a+Slave+4+U" itemprop="url">I'm a Slave 4 U</a>
</h3>
<p class="column-tracks-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Britney+Spears" itemprop="url">Britney Spears</a>
</span>
</p>
<div class="media-item">
<span class="column-tracks-item-image cover-art">
<img alt="Greatest Hits: My Prerogative" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/1cdb892aa1e6d29b749ff81bd7b92701.jpg"/>
</span>
<a class="column-tracks-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Britney Spears" data-artist-url="/music/Britney+Spears" data-playlink-affiliate="youtube" data-track-name="I'm a Slave 4 U" data-track-url="/music/Britney+Spears/_/I%27m+a+Slave+4+U" data-youtube-id="Mzybwwf2HoQ" data-youtube-url="https://www.youtube.com/watch?v=Mzybwwf2HoQ" href="https://www.youtube.com/watch?v=Mzybwwf2HoQ" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Britney+Spears/_/I%27m+a+Slave+4+U" tabindex="-1"></a>
</div>
</li>
<li class="column-tracks-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="column-tracks-item js-link-block link-block">
<h3 class="column-tracks-item-name" itemprop="name">
<a class="link-block-target" href="/music/The+Pussycat+Dolls/_/Buttons" itemprop="url">Buttons</a>
</h3>
<p class="column-tracks-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/The+Pussycat+Dolls" itemprop="url">The Pussycat Dolls</a>
</span>
</p>
<div class="media-item">
<span class="column-tracks-item-image cover-art">
<img alt="PCD" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/7c9048f891364c56a93ebe77be62dad6.jpg"/>
</span>
<a class="column-tracks-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="The Pussycat Dolls" data-artist-url="/music/The+Pussycat+Dolls" data-playlink-affiliate="youtube" data-track-name="Buttons" data-track-url="/music/The+Pussycat+Dolls/_/Buttons" data-youtube-id="VCLxJd1d84s" data-youtube-url="https://www.youtube.com/watch?v=VCLxJd1d84s" href="https://www.youtube.com/watch?v=VCLxJd1d84s" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/The+Pussycat+Dolls/_/Buttons" tabindex="-1"></a>
</div>
</li>
<li class="column-tracks-item-wrap column-tracks-item-wrap--end" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="column-tracks-item js-link-block link-block">
<h3 class="column-tracks-item-name" itemprop="name">
<a class="link-block-target" href="/music/Rihanna/_/Rude+Boy" itemprop="url">Rude Boy</a>
</h3>
<p class="column-tracks-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Rihanna" itemprop="url">Rihanna</a>
</span>
</p>
<div class="media-item">
<span class="column-tracks-item-image cover-art">
<img alt="Rated R" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/eb975424a267480276e7da24eb0e0231.jpg"/>
</span>
<a class="column-tracks-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Rihanna" data-artist-url="/music/Rihanna" data-playlink-affiliate="youtube" data-track-name="Rude Boy" data-track-url="/music/Rihanna/_/Rude+Boy" data-youtube-id="e82VE8UtW8A" data-youtube-url="https://www.youtube.com/watch?v=e82VE8UtW8A" href="https://www.youtube.com/watch?v=e82VE8UtW8A" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Rihanna/_/Rude+Boy" tabindex="-1"></a>
</div>
</li>
<li class="column-tracks-item-wrap column-tracks-item-wrap--end" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="column-tracks-item js-link-block link-block">
<h3 class="column-tracks-item-name" itemprop="name">
<a class="link-block-target" href="/music/Britney+Spears/_/Gimme+More" itemprop="url">Gimme More</a>
</h3>
<p class="column-tracks-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Britney+Spears" itemprop="url">Britney Spears</a>
</span>
</p>
<div class="media-item">
<span class="column-tracks-item-image cover-art">
<img alt="Blackout" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/b9a14a64aed91932f0f45708d6b20a74.jpg"/>
</span>
<a class="column-tracks-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Britney Spears" data-artist-url="/music/Britney+Spears" data-playlink-affiliate="youtube" data-track-name="Gimme More" data-track-url="/music/Britney+Spears/_/Gimme+More" data-youtube-id="elueA2rofoo" data-youtube-url="https://www.youtube.com/watch?v=elueA2rofoo" href="https://www.youtube.com/watch?v=elueA2rofoo" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Britney+Spears/_/Gimme+More" tabindex="-1"></a>
</div>
</li>
<li class="column-tracks-item-wrap column-tracks-item-wrap--end" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="column-tracks-item js-link-block link-block">
<h3 class="column-tracks-item-name" itemprop="name">
<a class="link-block-target" href="/music/The+Pussycat+Dolls/_/Don%27t+Cha" itemprop="url">Don't Cha</a>
</h3>
<p class="column-tracks-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/The+Pussycat+Dolls" itemprop="url">The Pussycat Dolls</a>
</span>
</p>
<div class="media-item">
<span class="column-tracks-item-image cover-art">
<img alt="PCD" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/7c9048f891364c56a93ebe77be62dad6.jpg"/>
</span>
<a class="column-tracks-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="The Pussycat Dolls" data-artist-url="/music/The+Pussycat+Dolls" data-playlink-affiliate="youtube" data-track-name="Don't Cha" data-track-url="/music/The+Pussycat+Dolls/_/Don%27t+Cha" data-youtube-id="YNSxNsr4wmA" data-youtube-url="https://www.youtube.com/watch?v=YNSxNsr4wmA" href="https://www.youtube.com/watch?v=YNSxNsr4wmA" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/The+Pussycat+Dolls/_/Don%27t+Cha" tabindex="-1"></a>
</div>
</li>
</ol>
</section>
</div>
<div class="col-sidebar">
<div class="tonefuze tonefuze--desktop hidden-xs" data-require="
                ads/tonefuze

            " data-tonefuze-artist="Beyoncé" data-tonefuze-flex="False" data-tonefuze-id="100000054" data-tonefuze-track="Naughty Girl" id="tonefuze-desktop">
</div>
<section class="buffer-standard hidden-xs">
<h3 class="text-18">Similar Tracks</h3>
<ol class="similar-items-sidebar similar-items-sidebar--with-3">
<li class="similar-items-sidebar-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="similar-items-sidebar-item js-link-block link-block">
<h3 class="similar-items-sidebar-item-name" itemprop="name">
<a class="link-block-target" href="/music/Beyonc%C3%A9/_/Baby+Boy+(feat.+Sean+Paul)" itemprop="url">Baby Boy (feat. Sean Paul)</a>
</h3>
<p class="similar-items-sidebar-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Beyonc%C3%A9" itemprop="url">Beyoncé</a>
</span>
</p>
<div class="media-item">
<span class="similar-items-sidebar-item-image cover-art">
<img alt="Baby Boy - Single" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/b27d7355750013c04ca5259d44357da3.jpg"/>
</span>
<a class="similar-items-sidebar-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Beyoncé" data-artist-url="/music/Beyonc%C3%A9" data-playlink-affiliate="youtube" data-track-name="Baby Boy (feat. Sean Paul)" data-track-url="/music/Beyonc%C3%A9/_/Baby+Boy+(feat.+Sean+Paul)" data-youtube-id="8ucz_pm3LX8" data-youtube-url="https://www.youtube.com/watch?v=8ucz_pm3LX8" href="https://www.youtube.com/watch?v=8ucz_pm3LX8" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Beyonc%C3%A9/_/Baby+Boy+(feat.+Sean+Paul)" tabindex="-1"></a>
</div>
</li>
<li class="similar-items-sidebar-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="similar-items-sidebar-item js-link-block link-block">
<h3 class="similar-items-sidebar-item-name" itemprop="name">
<a class="link-block-target" href="/music/Beyonc%C3%A9/_/Me,+Myself+and+I" itemprop="url">Me, Myself and I</a>
</h3>
<p class="similar-items-sidebar-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Beyonc%C3%A9" itemprop="url">Beyoncé</a>
</span>
</p>
<div class="media-item">
<span class="similar-items-sidebar-item-image cover-art">
<img alt="Dangerously in Love" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/60978eaf2b29dcee28301eb6fa21a3f5.jpg"/>
</span>
<a class="similar-items-sidebar-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Beyoncé" data-artist-url="/music/Beyonc%C3%A9" data-playlink-affiliate="youtube" data-track-name="Me, Myself and I" data-track-url="/music/Beyonc%C3%A9/_/Me,+Myself+and+I" data-youtube-id="4S37SGxZSMc" data-youtube-url="https://www.youtube.com/watch?v=4S37SGxZSMc" href="https://www.youtube.com/watch?v=4S37SGxZSMc" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Beyonc%C3%A9/_/Me,+Myself+and+I" tabindex="-1"></a>
</div>
</li>
<li class="similar-items-sidebar-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="similar-items-sidebar-item js-link-block link-block">
<h3 class="similar-items-sidebar-item-name" itemprop="name">
<a class="link-block-target" href="/music/Destiny%27s+Child/_/Lose+My+Breath" itemprop="url">Lose My Breath</a>
</h3>
<p class="similar-items-sidebar-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Destiny%27s+Child" itemprop="url">Destiny's Child</a>
</span>
</p>
<div class="media-item">
<span class="similar-items-sidebar-item-image cover-art">
<img alt="Destiny Fulfilled" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/0e3fecb01f78d0ced91432e3a77be2eb.jpg"/>
</span>
<a class="similar-items-sidebar-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Destiny's Child" data-artist-url="/music/Destiny%27s+Child" data-playlink-affiliate="youtube" data-track-name="Lose My Breath" data-track-url="/music/Destiny%27s+Child/_/Lose+My+Breath" data-youtube-id="AqeIiF0DlTg" data-youtube-url="https://www.youtube.com/watch?v=AqeIiF0DlTg" href="https://www.youtube.com/watch?v=AqeIiF0DlTg" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Destiny%27s+Child/_/Lose+My+Breath" tabindex="-1"></a>
</div>
</li>
</ol>
<button aria-controls="more-similar-tracks" aria-expanded="false" class="more-items" data-disclose-remove="">Show more</button>
<ol class="disclose-hide similar-items-sidebar similar-items-sidebar--with-9" id="more-similar-tracks">
<li class="similar-items-sidebar-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="similar-items-sidebar-item js-link-block link-block">
<h3 class="similar-items-sidebar-item-name" itemprop="name">
<a class="link-block-target" href="/music/Destiny%27s+Child/_/Bootylicious" itemprop="url">Bootylicious</a>
</h3>
<p class="similar-items-sidebar-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Destiny%27s+Child" itemprop="url">Destiny's Child</a>
</span>
</p>
<div class="media-item">
<span class="similar-items-sidebar-item-image cover-art">
<img alt="Survivor" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/fe3b5b68d86d157e7f55ea341e5a56a4.jpg"/>
</span>
<a class="similar-items-sidebar-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Destiny's Child" data-artist-url="/music/Destiny%27s+Child" data-playlink-affiliate="youtube" data-track-name="Bootylicious" data-track-url="/music/Destiny%27s+Child/_/Bootylicious" data-youtube-id="IyYnnUcgeMc" data-youtube-url="https://www.youtube.com/watch?v=IyYnnUcgeMc" href="https://www.youtube.com/watch?v=IyYnnUcgeMc" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Destiny%27s+Child/_/Bootylicious" tabindex="-1"></a>
</div>
</li>
<li class="similar-items-sidebar-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="similar-items-sidebar-item js-link-block link-block">
<h3 class="similar-items-sidebar-item-name" itemprop="name">
<a class="link-block-target" href="/music/Beyonc%C3%A9+&amp;+Shakira/_/Beautiful+Liar" itemprop="url">Beautiful Liar</a>
</h3>
<p class="similar-items-sidebar-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Beyonc%C3%A9+&amp;+Shakira" itemprop="url">Beyoncé &amp; Shakira</a>
</span>
</p>
<div class="media-item">
<span class="similar-items-sidebar-item-image cover-art">
<img alt="Hit Connection Best Of 2007" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/229e3184a77542f9cc01bd15a3f2658c.jpg"/>
</span>
<a class="similar-items-sidebar-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Beyoncé &amp; Shakira" data-artist-url="/music/Beyonc%C3%A9+&amp;+Shakira" data-playlink-affiliate="youtube" data-track-name="Beautiful Liar" data-track-url="/music/Beyonc%C3%A9+&amp;+Shakira/_/Beautiful+Liar" data-youtube-id="QrOe2h9RtWI" data-youtube-url="https://www.youtube.com/watch?v=QrOe2h9RtWI" href="https://www.youtube.com/watch?v=QrOe2h9RtWI" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Beyonc%C3%A9+&amp;+Shakira/_/Beautiful+Liar" tabindex="-1"></a>
</div>
</li>
<li class="similar-items-sidebar-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="similar-items-sidebar-item js-link-block link-block">
<h3 class="similar-items-sidebar-item-name" itemprop="name">
<a class="link-block-target" href="/music/Nicki+Minaj/_/Feeling+Myself" itemprop="url">Feeling Myself</a>
</h3>
<p class="similar-items-sidebar-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Nicki+Minaj" itemprop="url">Nicki Minaj</a>
</span>
</p>
<div class="media-item">
<span class="similar-items-sidebar-item-image cover-art">
<img alt="The Pinkprint (Deluxe)" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/ae4a60ffc368d5d0081673c9b6d9f91c.jpg"/>
</span>
<a class="similar-items-sidebar-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Nicki Minaj" data-artist-url="/music/Nicki+Minaj" data-playlink-affiliate="youtube" data-track-name="Feeling Myself" data-track-url="/music/Nicki+Minaj/_/Feeling+Myself" data-youtube-id="0Kg9xRooTVk" data-youtube-url="https://www.youtube.com/watch?v=0Kg9xRooTVk" href="https://www.youtube.com/watch?v=0Kg9xRooTVk" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Nicki+Minaj/_/Feeling+Myself" tabindex="-1"></a>
</div>
</li>
<li class="similar-items-sidebar-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="similar-items-sidebar-item js-link-block link-block">
<h3 class="similar-items-sidebar-item-name" itemprop="name">
<a class="link-block-target" href="/music/Rihanna/_/Pon+de+Replay" itemprop="url">Pon de Replay</a>
</h3>
<p class="similar-items-sidebar-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Rihanna" itemprop="url">Rihanna</a>
</span>
</p>
<div class="media-item">
<span class="similar-items-sidebar-item-image cover-art">
<img alt="Music of the Sun" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/41ec6a7494a22ba0a1a99ad5763cc454.jpg"/>
</span>
<a class="similar-items-sidebar-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Rihanna" data-artist-url="/music/Rihanna" data-playlink-affiliate="youtube" data-track-name="Pon de Replay" data-track-url="/music/Rihanna/_/Pon+de+Replay" data-youtube-id="oEauWw9ZGrA" data-youtube-url="https://www.youtube.com/watch?v=oEauWw9ZGrA" href="https://www.youtube.com/watch?v=oEauWw9ZGrA" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Rihanna/_/Pon+de+Replay" tabindex="-1"></a>
</div>
</li>
<li class="similar-items-sidebar-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="similar-items-sidebar-item js-link-block link-block">
<h3 class="similar-items-sidebar-item-name" itemprop="name">
<a class="link-block-target" href="/music/Britney+Spears/_/I%27m+a+Slave+4+U" itemprop="url">I'm a Slave 4 U</a>
</h3>
<p class="similar-items-sidebar-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Britney+Spears" itemprop="url">Britney Spears</a>
</span>
</p>
<div class="media-item">
<span class="similar-items-sidebar-item-image cover-art">
<img alt="Greatest Hits: My Prerogative" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/1cdb892aa1e6d29b749ff81bd7b92701.jpg"/>
</span>
<a class="similar-items-sidebar-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Britney Spears" data-artist-url="/music/Britney+Spears" data-playlink-affiliate="youtube" data-track-name="I'm a Slave 4 U" data-track-url="/music/Britney+Spears/_/I%27m+a+Slave+4+U" data-youtube-id="Mzybwwf2HoQ" data-youtube-url="https://www.youtube.com/watch?v=Mzybwwf2HoQ" href="https://www.youtube.com/watch?v=Mzybwwf2HoQ" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Britney+Spears/_/I%27m+a+Slave+4+U" tabindex="-1"></a>
</div>
</li>
<li class="similar-items-sidebar-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="similar-items-sidebar-item js-link-block link-block">
<h3 class="similar-items-sidebar-item-name" itemprop="name">
<a class="link-block-target" href="/music/The+Pussycat+Dolls/_/Buttons" itemprop="url">Buttons</a>
</h3>
<p class="similar-items-sidebar-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/The+Pussycat+Dolls" itemprop="url">The Pussycat Dolls</a>
</span>
</p>
<div class="media-item">
<span class="similar-items-sidebar-item-image cover-art">
<img alt="PCD" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/7c9048f891364c56a93ebe77be62dad6.jpg"/>
</span>
<a class="similar-items-sidebar-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="The Pussycat Dolls" data-artist-url="/music/The+Pussycat+Dolls" data-playlink-affiliate="youtube" data-track-name="Buttons" data-track-url="/music/The+Pussycat+Dolls/_/Buttons" data-youtube-id="VCLxJd1d84s" data-youtube-url="https://www.youtube.com/watch?v=VCLxJd1d84s" href="https://www.youtube.com/watch?v=VCLxJd1d84s" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/The+Pussycat+Dolls/_/Buttons" tabindex="-1"></a>
</div>
</li>
<li class="similar-items-sidebar-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="similar-items-sidebar-item js-link-block link-block">
<h3 class="similar-items-sidebar-item-name" itemprop="name">
<a class="link-block-target" href="/music/Rihanna/_/Rude+Boy" itemprop="url">Rude Boy</a>
</h3>
<p class="similar-items-sidebar-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Rihanna" itemprop="url">Rihanna</a>
</span>
</p>
<div class="media-item">
<span class="similar-items-sidebar-item-image cover-art">
<img alt="Rated R" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/eb975424a267480276e7da24eb0e0231.jpg"/>
</span>
<a class="similar-items-sidebar-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Rihanna" data-artist-url="/music/Rihanna" data-playlink-affiliate="youtube" data-track-name="Rude Boy" data-track-url="/music/Rihanna/_/Rude+Boy" data-youtube-id="e82VE8UtW8A" data-youtube-url="https://www.youtube.com/watch?v=e82VE8UtW8A" href="https://www.youtube.com/watch?v=e82VE8UtW8A" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Rihanna/_/Rude+Boy" tabindex="-1"></a>
</div>
</li>
<li class="similar-items-sidebar-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="similar-items-sidebar-item js-link-block link-block">
<h3 class="similar-items-sidebar-item-name" itemprop="name">
<a class="link-block-target" href="/music/Britney+Spears/_/Gimme+More" itemprop="url">Gimme More</a>
</h3>
<p class="similar-items-sidebar-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/Britney+Spears" itemprop="url">Britney Spears</a>
</span>
</p>
<div class="media-item">
<span class="similar-items-sidebar-item-image cover-art">
<img alt="Blackout" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/b9a14a64aed91932f0f45708d6b20a74.jpg"/>
</span>
<a class="similar-items-sidebar-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="Britney Spears" data-artist-url="/music/Britney+Spears" data-playlink-affiliate="youtube" data-track-name="Gimme More" data-track-url="/music/Britney+Spears/_/Gimme+More" data-youtube-id="elueA2rofoo" data-youtube-url="https://www.youtube.com/watch?v=elueA2rofoo" href="https://www.youtube.com/watch?v=elueA2rofoo" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/Britney+Spears/_/Gimme+More" tabindex="-1"></a>
</div>
</li>
<li class="similar-items-sidebar-item-wrap" itemscope="" itemtype="http://schema.org/MusicRecording">
<div class="similar-items-sidebar-item js-link-block link-block">
<h3 class="similar-items-sidebar-item-name" itemprop="name">
<a class="link-block-target" href="/music/The+Pussycat+Dolls/_/Don%27t+Cha" itemprop="url">Don't Cha</a>
</h3>
<p class="similar-items-sidebar-item-artist" itemprop="byArtist" itemscope="" itemtype="http://schema.org/MusicGroup">
<span itemprop="name">
<a href="/music/The+Pussycat+Dolls" itemprop="url">The Pussycat Dolls</a>
</span>
</p>
<div class="media-item">
<span class="similar-items-sidebar-item-image cover-art">
<img alt="PCD" itemprop="image" loading="lazy" src="https://lastfm.freetls.fastly.net/i/u/300x300/7c9048f891364c56a93ebe77be62dad6.jpg"/>
</span>
<a class="similar-items-sidebar-item-playlink desktop-playlink js-playlink" data-analytics-action="PlayTrackOnPage" data-analytics-label="youtube" data-artist-name="The Pussycat Dolls" data-artist-url="/music/The+Pussycat+Dolls" data-playlink-affiliate="youtube" data-track-name="Don't Cha" data-track-url="/music/The+Pussycat+Dolls/_/Don%27t+Cha" data-youtube-id="YNSxNsr4wmA" data-youtube-url="https://www.youtube.com/watch?v=YNSxNsr4wmA" href="https://www.youtube.com/watch?v=YNSxNsr4wmA" target="_blank" title="Play on YouTube">

                    Play track

            </a>
</div>
<a aria-hidden="true" class="js-link-block-cover-link link-block-cover-link" href="/music/The+Pussycat+Dolls/_/Don%27t+Cha" tabindex="-1"></a>
</div>
</li>
</ol>
</section>
<div class="sidebar-ad-container buffer-standard" data-ad-container="">
<div class="mpu_plus_top lastfm-ad" data-ad="mpu_plus_top" data-ads-placement='{"id": "mpu_plus_top", "sizes": [[300, 250], [300, 600]], "targeting": {"pos": "middle1"}, "adblock_message": true}' id="mpu_plus_top">
</div>
<p class="mpu-subscription-upsell mpu-subscription-upsell--mpu">
                Don't want to see ads? <a data-analytics-action="SubscribeClick" data-analytics-label="AdUpsellCTA" href="/pro">Upgrade Now</a>
</p>
</div>
<div class="related-ads">
<div data-searchlinks-desktop=""></div>
</div>
</div>
</div>
</div>
<div class="trending-tracks-section-wrapper" data-lazy-load-content="/charts/partial/trending-tracks" data-lazy-load-when-on-screen="" data-require="components/lazy-load-v3">
<section class="trending-tracks-section">
<div class="container">
<h3 class="text-18">Trending Tracks</h3>
<ul class="trending-tracks">
<li class="trending-tracks-item-wrap">
<div class="trending-tracks-item">
<p class="trending-tracks-item-index">
                            1
                        </p>
<div class="trending-tracks-album-art media-item">
<div class="cover-art--placeholder">
</div>
</div>
</div>
</li>
<li class="trending-tracks-item-wrap">
<div class="trending-tracks-item">
<p class="trending-tracks-item-index">
                            2
                        </p>
<div class="trending-tracks-album-art media-item">
<div class="cover-art--placeholder">
</div>
</div>
</div>
</li>
<li class="trending-tracks-item-wrap">
<div class="trending-tracks-item">
<p class="trending-tracks-item-index">
                            3
                        </p>
<div class="trending-tracks-album-art media-item">
<div class="cover-art--placeholder">
</div>
</div>
</div>
</li>
<li class="trending-tracks-item-wrap">
<div class="trending-tracks-item">
<p class="trending-tracks-item-index">
                            4
                        </p>
<div class="trending-tracks-album-art media-item">
<div class="cover-art--placeholder">
</div>
</div>
</div>
</li>
<li class="trending-tracks-item-wrap">
<div class="trending-tracks-item">
<p class="trending-tracks-item-index">
                            5
                        </p>
<div class="trending-tracks-album-art media-item">
<div class="cover-art--placeholder">
</div>
</div>
</div>
</li>
<li class="trending-tracks-item-wrap">
<div class="trending-tracks-item">
<p class="trending-tracks-item-index">
                            6
                        </p>
<div class="trending-tracks-album-art media-item">
<div class="cover-art--placeholder">
</div>
</div>
</div>
</li>
</ul>
<p class="trending-tracks-more-link">
<a href="/charts">View all trending tracks</a>
</p>
</div>
</section>
</div>
<div class="container page-content">
<div class="lazy-features-page-bottom" data-lazy-load-content="/features/partial/page-bottom?artist_url=/music/Beyonc%C3%A9" data-lazy-load-when-on-screen="" data-require="components/lazy-load-v3">
<div class="features-page-bottom section-with-separator section-with-separator--xs-only">
<h2 class="text-18">Features</h2>
<ul class="features-teasers">
<li class="features-teaser-wrap">
<div class="features-teaser">
<div class="features-teaser-image-outer">
<div class="features-teaser-image--placeholder"></div>
</div>
</div>
</li>
<li class="features-teaser-wrap">
<div class="features-teaser">
<div class="features-teaser-image-outer">
<div class="features-teaser-image--placeholder"></div>
</div>
</div>
</li>
<li class="features-teaser-wrap">
<div class="features-teaser">
<div class="features-teaser-image-outer">
<div class="features-teaser-image--placeholder"></div>
</div>
</div>
</li>
<li class="features-teaser-wrap">
<div class="features-teaser">
<div class="features-teaser-image-outer">
<div class="features-teaser-image--placeholder"></div>
</div>
</div>
</li>
</ul>
</div>
</div>
</div>
<div class="full-bleed-ad-container" data-ad-container="">
<div class="leader_bottom lastfm-ad" data-ad="leader_bottom" data-ads-placement='{"id": "leader_bottom", "sizes": [[728, 90], [970, 66], [728, 92]], "targeting": {"pos": "bottom"}}' id="leader_bottom">
</div>
</div>
<div class="container page-content visible-xs">
<div class="related-ads">
<div data-searchlinks-mobile=""></div>
</div>
</div>
</div>
<div id="qa-page-load"></div>
<footer class="footer" itemscope="" itemtype="http://schema.org/Organization">
<link href="https://www.last.fm" itemprop="url"/>
<div class="footer-top">
<div class="container">
<div class="footer-top-row">
<div class="footer-top-col">
<h2 class="footer-heading">Company</h2>
<ul class="footer-links">
<li><a href="/about">About Last.fm</a></li>
<li><a href="/about/contact">Contact Us</a></li>
<li><a href="/about/jobs">Jobs</a></li>
</ul>
</div>
<div class="footer-top-col">
<h2 class="footer-heading">Help</h2>
<ul class="footer-links">
<li><a href="/about/trackmymusic">Track My Music</a></li>
<li><a href="https://support.last.fm/" target="_BLANK">Community Support</a></li>
<li><a href="/help/guidelines">Community Guidelines</a></li>
<li><a href="/help/faq" target="_BLANK">Help</a></li>
</ul>
</div>
<div class="footer-top-col">
<h2 class="footer-heading">Goodies</h2>
<ul class="footer-links">
<li><a href="/about/trackmymusic">Download Scrobbler</a></li>
<li><a href="/api">Developer API</a></li>
<li><a href="/music/+free-music-downloads">Free Music Downloads</a></li>
<li><a href="https://store.last.fm">Merchandise</a></li>
</ul>
</div>
<div class="footer-top-col">
<h2 class="footer-heading">Account</h2>
<ul class="footer-links">
<li><a href="/join">Sign Up</a></li>
<li><a href="/login">Log In</a></li>
<li><a href="/pro">Subscribe</a></li>
</ul>
</div>
<div class="footer-top-col">
<h2 class="footer-heading">Follow Us</h2>
<ul class="footer-links">
<li><a href="https://www.facebook.com/lastfm" itemprop="sameAs" target="_blank">Facebook</a></li>
<li><a href="https://twitter.com/lastfm" itemprop="sameAs" target="_blank">Twitter</a></li>
<li><a href="https://www.instagram.com/last_fm" itemprop="sameAs" target="_blank">Instagram</a></li>
<li><a href="https://www.youtube.com/user/lastfm" itemprop="sameAs" target="_blank">YouTube</a></li>
</ul>
</div>
</div>
</div>
</div>
<div class="footer-bottom">
<div class="container">
<div class="row">
<div class="col-xs-12 col-sm-9">
<ul id="language-selector">
<li class="footer-language footer-language--active">
<strong>English</strong><span class="sr-only">current language</span>
</li>
<li class="footer-language">
<form action="/i18n/setlang/" class="footer-language-form" method="post">
<input name="language" type="hidden" value="de"/>
<button class="mimic-link" name="de" type="submit">Deutsch</button>
</form>
</li>
<li class="footer-language">
<form action="/i18n/setlang/" class="footer-language-form" method="post">
<input name="language" type="hidden" value="es"/>
<button class="mimic-link" name="es" type="submit">Español</button>
</form>
</li>
<li class="footer-language">
<form action="/i18n/setlang/" class="footer-language-form" method="post">
<input name="language" type="hidden" value="fr"/>
<button class="mimic-link" name="fr" type="submit">Français</button>
</form>
</li>
<li class="footer-language">
<form action="/i18n/setlang/" class="footer-language-form" method="post">
<input name="language" type="hidden" value="it"/>
<button class="mimic-link" name="it" type="submit">Italiano</button>
</form>
</li>
<li class="footer-language">
<form action="/i18n/setlang/" class="footer-language-form" method="post">
<input name="language" type="hidden" value="ja"/>
<button class="mimic-link" name="ja" type="submit">日本語</button>
</form>
</li>
<li class="footer-language">
<form action="/i18n/setlang/" class="footer-language-form" method="post">
<input name="language" type="hidden" value="pl"/>
<button class="mimic-link" name="pl" type="submit">Polski</button>
</form>
</li>
<li class="footer-language">
<form action="/i18n/setlang/" class="footer-language-form" method="post">
<input name="language" type="hidden" value="pt"/>
<button class="mimic-link" name="pt" type="submit">Português</button>
</form>
</li>
<li class="footer-language">
<form action="/i18n/setlang/" class="footer-language-form" method="post">
<input name="language" type="hidden" value="ru"/>
<button class="mimic-link" name="ru" type="submit">Русский</button>
</form>
</li>
<li class="footer-language">
<form action="/i18n/setlang/" class="footer-language-form" method="post">
<input name="language" type="hidden" value="sv"/>
<button class="mimic-link" name="sv" type="submit">Svenska</button>
</form>
</li>
<li class="footer-language">
<form action="/i18n/setlang/" class="footer-language-form" method="post">
<input name="language" type="hidden" value="tr"/>
<button class="mimic-link" name="tr" type="submit">Türkçe</button>
</form>
</li>
<li class="footer-language">
<form action="/i18n/setlang/" class="footer-language-form" method="post">
<input name="language" type="hidden" value="zh"/>
<button class="mimic-link" name="zh" type="submit">简体中文</button>
</form>
</li>
</ul>
<p class="footer-timezone">
<span data-lazy-load-content="/timezone" data-lazy-load-error-message="Timezone could not be loaded, try reloading the page." data-require="components/lazy-load-v3">
</span>
</p>
<div class="footer-legal">
<ul>
<li class="footer-legal-item"><a href="http://www.cbsinteractive.com/" rel="nofollow">CBS Interactive</a> © 2023 <span itemprop="name">Last.fm</span> Ltd. All rights reserved</li>
<li class="footer-legal-item"><a href="/legal/terms">Terms of Use</a></li>
<li class="footer-legal-item"><a href="/legal/privacy">Privacy Policy</a></li>
<li class="footer-legal-item"><a href="/legal">Legal Policies</a></li>
<li class="footer-legal-item"><a class="ot-sdk-show-settings">Do Not Sell My Personal Information</a></li>
<li class="footer-legal-item"><a href="https://careers.viacomcbs.com/" target="_blank">Jobs at ViacomCBS</a></li>
<li class="footer-legal-item"><a href="http://www.last.fm" rel="nofollow">Last.fm Music</a></li>
</ul>
</div>
</div>
<div class="logo col-xs-12 col-sm-3">
<p>Audioscrobbler</p>
<img alt="Last.fm 'as' logo" height="20" loading="lazy" src="/static/images/footer_logo@2x.49ca51948b0a.png" width="37"/>
</div>
</div>
</div>
</div>
</footer>
<section class="debug-log">
<h2 class="debug-log-heading">API Calls</h2>
</section>
</div>
<div data-ads-beacon="" data-ads-env="prod" data-ads-network="8264" data-ads-targeting='{"lang": "en", "beta": "yes", "ptype": "music_track_tags_overview", "artist": "beyonc\u00e9", "ar": "beyonc\u00e9", "tag": "rnb,sexy,pop,beyonce,femalevocalists,hip-hop"}' data-ads-zone="/music/track/tags/overview" id="data-ads"></div>
</div>
<div data-require="player/providers/spotify/spotify-provider" data-spotify-auth-modal="/player/modal/spotify" data-spotify-inactive-modal="/player/modal/spotify-inactive" data-spotify-initial-device-modal="/player/modal/spotify-initial-device-detection" data-spotify-premium-modal="/player/modal/spotify-premium"></div>
<div aria-hidden="true" class="video-player" data-require="player/providers/youtube/youtube-provider" id="youtube-video">
<div class="video-player-inner-wrap">
<div class="video-player-embed js-player"></div>
<button class="video-player-close js-close-player">Close</button>
</div>
</div>
<div class="tonefuze tonefuze--mobile visible-xs sticky-ad-container tonefuze-mobile" data-require="
                ads/tonefuze

                    , ads/ad-placement-helper

            " data-tonefuze-artist="Beyoncé" data-tonefuze-flex="False" data-tonefuze-id="100001211" data-tonefuze-track="Naughty Girl" id="tonefuze-mobile">
<button aria-controls="tonefuze-mobile" aria-expanded="true" class="disclose-trigger disclose-active" data-disclose-autoclose="" id="sticky-ad-disclose-button">
                    Close
                </button>
</div>
<script class="js-modal-template" type="text/template">
            <div class="modal-dialog" role="dialog" aria-labelledby="modal-label">
                <div class="modal-content" data-require="stats/base-v3">
                    <div class="modal-actions">

                        <button class="modal-dismiss js-close sr-only">Close</button>
                    </div>
                    <div js-modal-body class="modal-body">
                    </div>
                </div>
            </div>
        </script>
<script>
            var immediateUseBidBarrelFunctions = ['auction', 'initialize', 'setTargeting', 'destroySlots', 'setConfig', 'on', 'setLazyLoad'];
            (function(a){
                var w=window,b='BidBarrel',q='queue';w[b]=w[b]?w[b]:{};w[b][q]=w[b][q]?w[b][q]:[];
                a.forEach(function(z){w[b][z]=w[b][z]||function(){var c=arguments;w[b][q].push(function(r){w[b][z].apply(w[b],c);r()})}});
            })(immediateUseBidBarrelFunctions);
        </script><script async="" id="bb-lib" src="https://at.cbsi.com/lib/dist/prod/bidbarrel-lastfm.min.js"></script>
<script class="js-adblock-message-template" type="text/template">


    <div><div>
        <section class="
            adblock-message
            adblock-message--adfree
            link-block
            js-link-block
        ">
            <p class="adblock-message-body">

                    <strong>Browse ad-free</strong> with a premium Last.fm account

            </p>

            <a
                class="adblock-message-button link-block-target"
                href="/pro"
                data-analytics-action="SubscribeClick"
                data-analytics-label="AdblockMessageAdfree"
            >Find out more</a>
            <a
                href="/pro"
                class="
                    js-link-block-cover-link
                    link-block-cover-link
                "
                tabindex="-1"
                aria-hidden="true"
                data-analytics-action="SubscribeClick"
                data-analytics-label="AdblockMessageAdfree"
            ></a>
        </section>
    </div></div>

            </script>
<script class="js-adblock-message-template" type="text/template">


    <div><div>
        <section class="
            adblock-message
            adblock-message--support
            link-block
            js-link-block
        ">
            <p class="adblock-message-body">

                    <strong>Show your support</strong> with a premium Last.fm account

            </p>

            <a
                class="adblock-message-button link-block-target"
                href="/pro"
                data-analytics-action="SubscribeClick"
                data-analytics-label="AdblockMessageSupport"
            >Find out more</a>
            <a
                href="/pro"
                class="
                    js-link-block-cover-link
                    link-block-cover-link
                "
                tabindex="-1"
                aria-hidden="true"
                data-analytics-action="SubscribeClick"
                data-analytics-label="AdblockMessageSupport"
            ></a>
        </section>
    </div></div>

            </script>
<script class="js-adblock-message-template" type="text/template">


    <div><div>
        <section class="
            adblock-message
            adblock-message--benefits
            link-block
            js-link-block
        ">
            <p class="adblock-message-body">

                    <strong>Get exclusive benefits</strong> with a premium Last.fm account

            </p>

            <a
                class="adblock-message-button link-block-target"
                href="/pro"
                data-analytics-action="SubscribeClick"
                data-analytics-label="AdblockMessageBenefits"
            >Find out more</a>
            <a
                href="/pro"
                class="
                    js-link-block-cover-link
                    link-block-cover-link
                "
                tabindex="-1"
                aria-hidden="true"
                data-analytics-action="SubscribeClick"
                data-analytics-label="AdblockMessageBenefits"
            ></a>
        </section>
    </div></div>

            </script>
<script>
            window.lfmDomReadyCallback && window.lfmDomReadyCallback();
            window.lfmDomReady = true;
        </script>
<link as="style" charset="utf-8" data-require="shim/rel-preload" href="/static/styles/build/app-84b2a7e256.4630aa8be3f9.css" media="(min-width: 768px)" rel="preload"/>
</body>
</html>"""

def base_url():
    return 'https://www.last.fm/music/'

def get_param_string(param_word_list):
    return '+'.join(param_word_list)

def get_url_string(artist_name, song_name):
    #artist = get_param_string(artist_name)
    #s_name = get_param_string(song_name)
    return 'https://www.last.fm/music/{}/_/{}/+tags'.format(artist_name, song_name)

class LastFM(Proxy_Checker):

    def __init__(self):
        Proxy_Checker.__init__(self, "lastfm", base_url())
        self.base_url = base_url()
        self.url_max_retrires = 5
        self.max_retries = 5
        self.max_workers = 100
        self.timeout = 10
        
        self.lastfm_link_data = 'lastfm_data_to_scrap.json'
        self.lastfm_link_genre = 'data_genres.json'
        self.az_lyrics_data = 'data_lyrics.json'
        self.lastfm_load_data()
        self.az_logger()

    def lastfm_load_data(self):
        self.lastfm_data = json.load(open(os.path.abspath(self.lastfm_link_data) , 'r'))
        self.lastfm_genre = json.load(open(os.path.abspath(self.lastfm_link_genre) , 'r'))
        self.song_data = json.load(open(os.path.abspath(self.az_lyrics_data) , 'r'))

    def az_logger(self):
        self.az_logger = logging.getLogger(__name__)
        self.az_logger.setLevel(logging.DEBUG)
        self.az_formatter = logging.Formatter('%(asctime)s : %(filename)s : %(funcName)s : %(levelname)s : %(message)s')
        self.az_file_handler = logging.FileHandler(os.path.abspath('main.log'))
        self.az_file_handler.setLevel(logging.DEBUG)
        self.az_file_handler.setFormatter(self.az_formatter)
        self.az_logger.addHandler(self.az_file_handler)

    def save_lastfm_data(self):
        with open(self.lastfm_link_data, 'w') as outfile:
            json.dump(self.lastfm_data, outfile, indent=4)

    def save_lastfm_genre(self):
        with open(self.lastfm_link_genre , 'w') as outfile:
            json.dump(self.lastfm_genre , outfile, indent=4)

    """
    def get_url(self , url):
        flag = self.url_max_retrires
        while(flag):
            header = self.return_header()
            proxy = self.return_proxy()
            try:
                site = requests.get(url , headers = header , proxies = {'http':proxy,'https':proxy},timeout = self.timeout)
                if site.status_code == requests.codes.ok:
                    html_soup = BeautifulSoup(site.text , 'html.parser')
                    if len(html_soup.find_all('div',class_ = 'alert alert-info')) == 0:
                        self.az_logger.info('SuccessFul Get Request -> {} using Proxy -> {} on try-> {}'.format(url,proxy,flag))
                        flag=0
                        return html_soup
                    else:
                        self.az_logger.debug('Recapta Detected -> {} using Proxy -> {} on try-> {}'.format(url , proxy , flag))
                        flag -= 1
                        if flag == 0:
                            return '0'
                else:
                    self.az_logger.debug('Proxy Status Mismatch -> {} using Proxy -> {} on Try -> {}'.format(site.status_code , proxy , flag))
                    flag -= 1
                    if flag ==0:
                        return '0'
            except Exception as E:
                self.az_logger.debug('Something Went Wrong -> {} using  Proxy -> {} Error -> {} on try-> {}'.format(url,proxy,E,flag))
                flag -= 1
                if flag == 0:
                    return '0'
        return '0'"""

    """
    def lastfm_genre_by_list(self , mode = 'Existing'):
        if mode == 'New':
            self.lastfm_data['scrap_genre_success'] = []
            self.lastfm_data['simple_urls'] = []
            #self.lastfm_data['songs_details'] = []
            #self.lastfm_data['albums_details'] = []
            flag = 0
        if mode == 'Existing':
            flag = self.lastfm_data['flag']
            
        temp_flag = self.max_retries
        while(temp_flag):
            for url in self.lastfm_data['scrap_by_singer']:
                if url not in self.lastfm_data['scrap_genre_success']:
                    try:
                        html_soup = self.get_url(url)
                        if html_soup != '0':
                            title = html_soup.find('h1').text
                            songs = html_soup.find_all('div',class_ = 'listalbum-item')
                            albums = html_soup.find_all('div', class_ = 'album')
                            for album in albums:
                                album_id = album.get('id')
                                album_name = album.b.text.replace('"','')
                                album_type = album.text.split(':')[0]
                                if re.search("\(([\d+]+)\)",album.text) is not None:
                                    album_year = re.findall("\(([\d+]+)\)",album.text)[0]
                                else:
                                    album_year = 'Not Defined'
                                #self.lastfm_data['albums_details'].append({'id': album_id,'singer_name':title,'name':album_name,'type':album_type,'year':album_year})
                            for song in songs:
                                song_href = song.a.get('href')
                                song_name = song.a.text
                                flag += 1
                                #self.lastfm_data['songs_details'].append({'song_id':flag ,'singer_name':title ,'song_name': song_name,'song_href': song_href})
                                self.lastfm_data['simple_urls'].append(song_href)
                            self.lastfm_data['scrap_genre_success'].append(url)
                            self.az_logger.info('SuccessFully Parsed the Request -> {}'.format(url))
                        else:
                            self.az_logger.debug('UnSuccessFul to Parse the Request -> {} ..!! Max Retries'.format(url))
                            # data['scrap_singer_unsuccess'].append(url)
                    except Exception as E:
                        self.az_logger.warning('Something Wrong while Requesting -> {} Error -> {} on line No. -> {}'.format(url,E,sys.exc_info()[-1].tb_lineno))
            temp_flag -= 1
        self.lastfm_data['flag'] = flag
        self.save_lastfm_data()"""
        
    def add_urls_from_lyric_data(self):
        if len(self.lastfm_data["simple_urls"]) == 0:
            for song_data in self.song_data["lyrics"]:
                temp_artist_name_list = song_data["artist"].split(" ")[:-1]
                temp_artist = " ".join(temp_artist_name_list)
                
                artist = temp_artist.replace(" ", "+")
                song_name = song_data["song_name"].replace(" ", "+")
                
                full_url = get_url_string(artist, song_name)
                
                self.lastfm_data["simple_urls"].append(full_url)
            self.save_lastfm_data()
        
        """
            1)open data_lyrics.json 
                get the artist name and the song name 
                
                "link": "https://www.azlyrics.com/lyrics/solangeknowles/dontfightthefeeling.html",
                "artist": "Solange Knowles Lyrics",
                "song_name": "Don't Fight The Feeling",
            2) format this to get a link for the song 
                format -> https://www.last.fm/music/{artist name (sperate with '+')}/_/{song name (sperate with '+')}/+tags
                'https://www.last.fm/music/{}/_/{}/+tags'.format(name, age)
            3)
                save urls to ["simple_urls"]
            4)
        
        
        """
        
    def get_scrape_data(self , url):
        flag = self.url_max_retrires
        while(flag):
            header = self.return_header()
            proxy = self.return_proxy()
            try:
                site = requests.get(url , headers = header , proxies = {'http':proxy,'https':proxy},timeout = self.timeout)
                if site.status_code == requests.codes.ok:
                    html_soup = BeautifulSoup(site.text , 'html.parser')
                    return html_soup
                    '''if len(html_soup.find_all('div',class_ = 'alert alert-info')) == 0:
                        self.az_logger.info('SuccessFul Get Request -> {} using Proxy -> {} on try-> {}'.format(url,proxy,flag))
                        flag=0
                        return html_soup
                    else:
                        self.az_logger.debug('Recapta Detected -> {} using Proxy -> {} on try-> {}'.format(url , proxy , flag))
                        flag -= 1
                        if flag == 0:
                            return '0'''
                else:
                    self.az_logger.debug('Proxy Status Mismatch -> {} using Proxy -> {} on Try -> {}'.format(site.status_code , proxy , flag))
                    flag -= 1
                    if flag ==0:
                        return '0'
            except Exception as E:
                self.az_logger.debug('Something Went Wrong -> {} using  Proxy -> {} Error -> {} on try-> {}'.format(url,proxy,E,flag))
                flag -= 1
                if flag == 0:
                    return '0'
        return '0'
        
    def genre_data_from_link(self , link):
        html_soup = self.get_scrape_data(link)
        #print(html_soup)
        
        #header = self.return_header()
        #proxy = self.return_proxy()
        #site = requests.get(url , headers = header , proxies = {'http':proxy,'https':proxy},timeout = self.timeout)
        #print(site)
        #if site.status_code == requests.codes.ok:
        #html_soup = BeautifulSoup(test_site_string() , 'html.parser')
        #else
            #print(html_soup)
            #return html_soup
        
        if html_soup != '0':
            try:
                song_name = html_soup.find('h1', class_='header-new-title').string
                
                genre_data_html = html_soup.find_all('h3' , class_ = 'big-tags-item-name')
                genre_data = []
                for genre in genre_data_html:
                    genre_data.append(genre.text.replace("\n", ""))
                #print(genre_data)
                artist = html_soup.find_all('span', itemprop="byArtist")[0].span.string
                #["itemprop"].find('span').string
                artist = unidecode(artist).lower()
                #print(artist)
                #class = header-new-content, attribute itemprop="byArtist", itemprop="name" , then get text
                
                if artist in genre_data:
                    genre_data.remove(artist)
                
                return {'link':link, 'artist':artist , 'song_name':song_name , 'genre_list': genre_data}
            except Exception as E:
                self.az_logger.warning('Error in Scrapping genres {} Lineno.->{}'.format(E , sys.exc_info()[-1].tb_lineno))
                return '0'
        else:
            return '0'
    

    def get_all_urls_not_updated(self):
        unsuccess = []
        for list_batch in self.lastfm_data['simple_urls']:
            if list_batch not in self.lastfm_genre['completed']:
                unsuccess.append(list_batch)
                
        print(len(unsuccess))
        
    
    async def get_batch_genres(self):
        #get all songs we did not 
        unsuccess = []
        for list_batch in self.lastfm_data['simple_urls']:
            if list_batch not in self.lastfm_genre['completed']:
                unsuccess.append(list_batch)
                
        self.az_logger.info('UnSuccessFul links {}'.format(unsuccess[0]))
        flag = self.max_retries
        while(flag):
            try:
                with ThreadPoolExecutor(max_workers = self.max_workers) as executor:
                    loop = asyncio.get_event_loop()
                    tasks = [
                            loop.run_in_executor(executor , self.genre_data_from_link , pro)
                            for pro in unsuccess
                    ]
                    for response in await asyncio.gather(*tasks):
                        if response != '0':
                            self.lastfm_genre['genres'].append(response)
                            self.lastfm_genre['completed'].append(response['link'])
                            unsuccess.remove(response['link'])
                    if len(unsuccess) == 0:
                        flag = 0
                    else:
                        flag -= 1
            except Exception as E:
                self.az_logger.warning('Scrapping Went Wrong -> {} Lineno. -> {}'.format(E , sys.exc_info()[-1].tb_lineno))
            finally:
                self.save_lastfm_genre()
        self.az_logger.info('Scrapped Successful... No. of genres in file is  {}'.format(len(self.lastfm_genre['completed'])))
        self.save_lastfm_genre()

    def start_scrapping(self):
        try:
            self.loop = asyncio.get_event_loop()
            self.loop.set_debug(1)
            future = asyncio.ensure_future(self.get_batch_genres())
            self.loop.run_until_complete(future)
        except Exception as E:
            self.az_logger.warning('Warning Log -> {} Lineno -> {}'.format(E, sys.exc_info()[-1].tb_lineno))
        finally:
            self.loop.close()

if __name__ == "__main__":

    last_fm = LastFM()
    #last_fm.get_all_urls_not_updated()
    
    #last_fm.lastfm_genre_by_list("New")
    #link = "https://www.last.fm/music/Beyonc%C3%A9/_/Naughty+Girl/+tags"
    #test = last_fm.genre_data_from_link(link)
    #print(test)
    #last_fm.start_scrapping()
    
    user = input("Enter command or 'help' : ")
    while user != 'end':
        
        if user == 'help':
            print("'gcount : get the count of remaining genere calls'")
            print("'gdata' : start collecting data")
            print("'end' : end script")
            
        elif user == 'gcount':
            last_fm.get_all_urls_not_updated()
            
        elif user == 'gdata':
            last_fm.start_scrapping()
            
        else:
            print("invlaid command : "+ user)
            
        user = input("Enter command or 'help' : ")  
            