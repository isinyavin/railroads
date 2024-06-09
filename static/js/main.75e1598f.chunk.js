(window.webpackJsonp=window.webpackJsonp||[]).push([[0],[,,,,function(e,t,a){e.exports=a.p+"static/media/3448683-1.6f1fe84c.png"},function(e,t,a){e.exports=a(19)},,,,,,,,function(e,t,a){},function(e,t,a){},function(e,t,a){},function(e,t,a){},,function(e,t,a){},function(e,t,a){"use strict";a.r(t);var n=a(0),o=a.n(n),c=a(3),l=a.n(c);a(13);var r=function(e){let{label:t,setSelectedGeography:a,selectedGeography:n}=e;return o.a.createElement("div",null,o.a.createElement("label",{htmlFor:"geography-select"},t),o.a.createElement("select",{id:"geography-select",value:n,onChange:e=>{a(e.target.value)}},o.a.createElement("option",{value:""},"Please Select a Geography"),o.a.createElement("option",{value:"uk"},"United Kingdom"),o.a.createElement("option",{value:"belgium"},"Belgium"),o.a.createElement("option",{value:"france"},"France"),o.a.createElement("option",{value:"italy"},"Italy")))};var s=e=>{let{routeImage:t}=e;return o.a.createElement("div",null,t?o.a.createElement("img",{src:t,alt:"Route Map",style:{width:"100%",height:"auto"}}):"Route map will be displayed here.")};a(14),a(15);var i=function(e){let{geography:t,placeholder:a,onSelect:c,selectedStation:l}=e;const[r,s]=Object(n.useState)([]),[i,m]=Object(n.useState)(!1),[u,d]=Object(n.useState)(null),[p,h]=Object(n.useState)([]),[E,g]=Object(n.useState)(""),[f,b]=Object(n.useState)(null);return Object(n.useEffect)(()=>{if(b(null),g(l||""),l){const e=r.find(e=>e.name===l);b(e||null)}},[l,r]),Object(n.useEffect)(()=>{t&&(async()=>{m(!0);try{const e=await fetch("https://railroads-production.up.railway.app/api/".concat(t,"/stations"));if(!e.ok)throw new Error("Something went wrong!");const a=await e.json();s(a)}catch(u){d(u.message)}m(!1)})()},[t]),o.a.createElement("div",{className:"search"},o.a.createElement("div",{className:"searchInputs"},o.a.createElement("input",{type:"text",placeholder:a,value:E,onChange:e=>{b(null);const t=e.target.value.toLowerCase();g(t);const a=r.filter(e=>e.name.toLowerCase().includes(t)||e.admin1&&e.admin1.toLowerCase().includes(t)||e.admin2&&e.admin2.toLowerCase().includes(t)||e.country&&e.country.toLowerCase().includes(t));h(""===t?[]:a)}})),f&&o.a.createElement("div",{className:"station-selected-details"},o.a.createElement("p",null,f.admin1,", ",f.admin2,", ",f.country)),0!==p.length&&o.a.createElement("div",{className:"dataResult"},i&&o.a.createElement("div",null,"Loading..."),u&&o.a.createElement("div",null,"Error: ",u),p.map((e,t)=>o.a.createElement("div",{key:t,className:"dataItem",onClick:()=>(e=>{const t=e.trim();g(t),h([]),c(e)})(e.name)},o.a.createElement("p",{className:"station-name"},e.name.trim()),o.a.createElement("p",{className:"station-details"},e.admin2,", ",e.admin1,", ",e.country)))))};a(16);var m=function(){return o.a.createElement("div",{className:"spinner-container"},o.a.createElement("div",{className:"loading-spinner"}))},u=a(1),d=a.n(u),p=(a(17),a(18),a(4)),h=a.n(p);var E=e=>{let{geo:t,depart:a,dest:c,startRouting:l,coordinates:r,stations:s,appearstations:i}=e;return Object(n.useEffect)(()=>{if(!l)return;if(!r&&!s)return;const e=d.a.map("map").setView([54.9679903,-2.4627642],8),t=d.a.icon({iconUrl:h.a,iconSize:[25,25],popupAnchor:[1,-34],shadowSize:[41,41]});d.a.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:19}).addTo(e);const a=r.map(e=>{const[t,a]=e.split(", ").map(Number);return[a,t]});if(a.length>1){const t=d.a.polyline(a,{color:"blue"}).addTo(e);e.fitBounds(t.getBounds())}else console.error("Insufficient data for route coordinates: ",a);return Array.isArray(s)?s.forEach((a,n)=>{const[o,c]=a.coordinates,l=0===n||n===s.length-1;if(l||i){let n=d.a.marker([c,o],{icon:t}).addTo(e);l?n.bindTooltip(a.name,{permanent:!0}).openTooltip():n.bindPopup(a.name)}}):console.error("stationsData is not an array:",s),()=>e.remove()},[t,a,c,l,r,s,i]),o.a.createElement("div",{id:"map",className:"map-container"})};var g=function(){const[e,t]=Object(n.useState)(""),[a,c]=Object(n.useState)(""),[l,u]=Object(n.useState)(""),[d,p]=Object(n.useState)(null),[h,g]=Object(n.useState)([]),[f,b]=Object(n.useState)(!1),[v,w]=Object(n.useState)(!1),[y,S]=Object(n.useState)(!1),[N,j]=Object(n.useState)(!1),[O,C]=Object(n.useState)(!0),[k,R]=Object(n.useState)(!1),[M,L]=Object(n.useState)([]),[x,I]=Object(n.useState)(""),[D,G]=Object(n.useState)(!1),T=()=>{S(!y)};return o.a.createElement("div",{className:"App"},o.a.createElement("header",{className:"App-header"},"RailRouter"),o.a.createElement("div",{className:"ContentwMap"},o.a.createElement("div",{className:"Content"},o.a.createElement("div",{className:"Selectors-wrapper"},o.a.createElement("div",{className:"Selectors"},o.a.createElement(r,{label:"Choose a geography",setSelectedGeography:c,selectedGeography:a}),o.a.createElement(i,{geography:a,placeholder:"Enter Departure Station",onSelect:t,selectedStation:e}),o.a.createElement(i,{geography:a,placeholder:"Enter Destination Station",onSelect:u,selectedStation:l}),o.a.createElement("button",{className:"random-station-generator",onClick:async()=>{if(a)try{const n=await fetch("https://railroads-production.up.railway.app/api/".concat(a,"/stations"));if(!n.ok)throw new Error("Failed to fetch stations");const o=await n.json();let c=Math.floor(Math.random()*o.length),l=Math.floor(Math.random()*o.length);for(;l===c;)l=Math.floor(Math.random()*o.length);t(o[c].name),u(o[l].name)}catch(e){console.error("Error fetching stations:",e),b(!1)}else alert("Please select a geography first.")}},"Generate Random Stations"),o.a.createElement("div",{className:"stationContainer"},o.a.createElement("div",{className:"textstations"},o.a.createElement("p",null,"Show Stations on Route")),o.a.createElement("button",{className:"toggle-btn ".concat(D?"toggled":""),onClick:()=>G(!D)},o.a.createElement("div",{className:"thumb"})))),o.a.createElement("button",{className:"find-route-button",onClick:async()=>{try{R(!0),S(!0),b(!0),w(!1),j(!0);const n=await fetch("https://railroads-production.up.railway.app/api/route/coords/".concat(a,"/").concat(e,"/").concat(l));if(!n.ok)throw new Error("Failed to fetch route coordinates");{const e=await n.json();L(e[0]),I(e[1])}const o=await fetch("https://railroads-production.up.railway.app/api/route/details/".concat(a,"/").concat(e,"/").concat(l));if(o.ok){const t=await o.json();b(!1),g(t);const n=await fetch("https://railroads-production.up.railway.app/api/route/".concat(a,"/").concat(e,"/").concat(l));if(n.ok){const e=await n.blob(),t=URL.createObjectURL(e);p(t),b(!1)}}else b(!1),w(!0),p(null),g([])}catch(t){b(!1),w(!0),p(null),g([])}}},"Find Route"),v&&o.a.createElement("div",{className:"error-box"},o.a.createElement("p",null,"No route exists between the two selected stations. Please try again.")),f&&o.a.createElement("div",{className:"loading-container"},o.a.createElement("p",null,"Loading map. This may take a while..."),o.a.createElement(m,null))),o.a.createElement("div",{className:"Output-Components"},!f&&N&&!v&&o.a.createElement("div",{className:"toggle-bar"},o.a.createElement("div",{className:"slider ".concat(!0===y?"left":"right")}),o.a.createElement("button",{className:"toggle-option ".concat(!0===y?"active":""),onClick:()=>T()},"Map"),o.a.createElement("button",{className:"toggle-option ".concat(!1===y?"active":""),onClick:()=>T()},"Details")),y&&!O&&o.a.createElement("div",{className:"MapContainer"},!f&&o.a.createElement(s,{routeImage:d})),y&&O&&o.a.createElement(E,{geo:a,depart:e,dest:l,startRouting:k,coordinates:M,stations:x,appearstations:D}),!y&&N&&!f&&o.a.createElement("div",{className:"RouteDetails"},o.a.createElement("h2",null,"Route Details"),h.length>0?o.a.createElement("ul",null,h.map((e,t)=>o.a.createElement("li",{key:t},e))):o.a.createElement("p",null,"No route details available."))))))};l.a.render(o.a.createElement(o.a.StrictMode,null,o.a.createElement(g,null)),document.getElementById("root"))}],[[5,1,2]]]);
//# sourceMappingURL=main.75e1598f.chunk.js.map