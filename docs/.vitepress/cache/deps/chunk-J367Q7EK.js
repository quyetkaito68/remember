import {
  getConfig2
} from "./chunk-FUE7ZNTF.js";
import {
  select_default
} from "./chunk-7Z52U4KA.js";
import {
  __name
} from "./chunk-DTCXZATX.js";

// node_modules/mermaid/dist/chunks/mermaid.core/chunk-VAUOI2AC.mjs
var selectSvgElement = __name((id) => {
  var _a;
  const { securityLevel } = getConfig2();
  let root = select_default("body");
  if (securityLevel === "sandbox") {
    const sandboxElement = select_default(`#i${id}`);
    const doc = ((_a = sandboxElement.node()) == null ? void 0 : _a.contentDocument) ?? document;
    root = select_default(doc.body);
  }
  const svg = root.select(`#${id}`);
  return svg;
}, "selectSvgElement");

export {
  selectSvgElement
};
//# sourceMappingURL=chunk-J367Q7EK.js.map
