import {
  parse
} from "./chunk-JL4YYJE3.js";
import "./chunk-QZNFD7EP.js";
import "./chunk-F7RPEPAU.js";
import "./chunk-AAYMC7FB.js";
import "./chunk-LSEGHARG.js";
import "./chunk-Z5PIV2M2.js";
import "./chunk-ZS2P4465.js";
import "./chunk-KNBVPU2O.js";
import "./chunk-UFHR6W3S.js";
import "./chunk-2CIAGU4W.js";
import "./chunk-AK6KVMQY.js";
import "./chunk-FYSQ6BLV.js";
import "./chunk-VCTPYKZT.js";
import "./chunk-LQYI5DSI.js";
import "./chunk-C2KOSO7Q.js";
import "./chunk-NBBJRPI2.js";
import "./chunk-EJGPZHPE.js";
import {
  selectSvgElement
} from "./chunk-J367Q7EK.js";
import {
  configureSvgSize
} from "./chunk-FUE7ZNTF.js";
import {
  log
} from "./chunk-7Z52U4KA.js";
import {
  __name
} from "./chunk-DTCXZATX.js";
import "./chunk-FFWGCFKV.js";
import "./chunk-EQCVQC35.js";

// node_modules/mermaid/dist/chunks/mermaid.core/infoDiagram-FWYZ7A6U.mjs
var parser = {
  parse: __name(async (input) => {
    const ast = await parse("info", input);
    log.debug(ast);
  }, "parse")
};
var DEFAULT_INFO_DB = {
  version: "11.16.0" + (true ? "" : "-tiny")
};
var getVersion = __name(() => DEFAULT_INFO_DB.version, "getVersion");
var db = {
  getVersion
};
var draw = __name((text, id, version) => {
  log.debug("rendering info diagram\n" + text);
  const svg = selectSvgElement(id);
  configureSvgSize(svg, 100, 400, true);
  const group = svg.append("g");
  group.append("text").attr("x", 100).attr("y", 40).attr("class", "version").attr("font-size", 32).style("text-anchor", "middle").text(`v${version}`);
}, "draw");
var renderer = { draw };
var diagram = {
  parser,
  db,
  renderer
};
export {
  diagram
};
//# sourceMappingURL=infoDiagram-FWYZ7A6U-DWRUHRXW.js.map
