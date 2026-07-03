import {
  db,
  getStyles,
  renderer
} from "./chunk-KT6JNEVW.js";
import {
  populateCommonDb
} from "./chunk-7ST5RZJI.js";
import {
  MermaidParseError
} from "./chunk-JL4YYJE3.js";
import "./chunk-QZNFD7EP.js";
import "./chunk-F7RPEPAU.js";
import "./chunk-AAYMC7FB.js";
import "./chunk-LSEGHARG.js";
import "./chunk-Z5PIV2M2.js";
import "./chunk-ZS2P4465.js";
import "./chunk-KNBVPU2O.js";
import {
  createRailroadServices
} from "./chunk-UFHR6W3S.js";
import "./chunk-2CIAGU4W.js";
import "./chunk-AK6KVMQY.js";
import "./chunk-FYSQ6BLV.js";
import "./chunk-VCTPYKZT.js";
import "./chunk-LQYI5DSI.js";
import "./chunk-C2KOSO7Q.js";
import "./chunk-NBBJRPI2.js";
import "./chunk-EJGPZHPE.js";
import "./chunk-J367Q7EK.js";
import "./chunk-FUE7ZNTF.js";
import {
  log
} from "./chunk-7Z52U4KA.js";
import {
  __name
} from "./chunk-DTCXZATX.js";
import "./chunk-FFWGCFKV.js";
import "./chunk-EQCVQC35.js";

// node_modules/mermaid/dist/chunks/mermaid.core/railroadDiagram-RFXS5EU6.mjs
var langiumParser = createRailroadServices().Railroad.parser.LangiumParser;
var transformExpression = __name((expr) => {
  switch (expr.$type) {
    case "RailroadTerminalExpr":
      return {
        type: "terminal",
        value: expr.value
      };
    case "RailroadNonTerminalExpr":
      return {
        type: "nonterminal",
        name: expr.name
      };
    case "RailroadSpecialExpr":
      return {
        type: "special",
        text: expr.text
      };
    case "RailroadSequenceExpr": {
      const elements = expr.elements.map(transformExpression);
      return elements.length === 1 ? elements[0] : { type: "sequence", elements };
    }
    case "RailroadChoiceExpr": {
      const alternatives = expr.alternatives.map(transformExpression);
      return alternatives.length === 1 ? alternatives[0] : { type: "choice", alternatives };
    }
    case "RailroadOptionalExpr":
      return {
        type: "optional",
        element: transformExpression(expr.element)
      };
    case "RailroadOneOrMoreExpr":
      return {
        type: "repetition",
        element: transformExpression(expr.element),
        min: 1,
        max: Infinity
      };
    case "RailroadZeroOrMoreExpr":
      return {
        type: "repetition",
        element: transformExpression(expr.element),
        min: 0,
        max: Infinity
      };
    default:
      throw new Error(`Unsupported railroad expression: ${expr.$type}`);
  }
}, "transformExpression");
var transformRule = __name((rule) => {
  return {
    name: rule.name,
    definition: transformExpression(rule.definition)
  };
}, "transformRule");
var populateDb = __name((ast) => {
  populateCommonDb(ast, db);
  if (ast.title) {
    db.setTitle(ast.title);
  }
  ast.rules.map((rule) => db.addRule(transformRule(rule)));
}, "populateDb");
var parser = {
  parse: __name((input) => {
    db.clear();
    log.debug("[Railroad Parser] Starting Langium parse");
    const result = langiumParser.parse(input);
    if (result.lexerErrors.length > 0 || result.parserErrors.length > 0) {
      throw new MermaidParseError(result);
    }
    const ast = result.value;
    log.debug("[Railroad Parser] Parsed rules:", ast.rules.length);
    populateDb(ast);
    log.debug("[Railroad Parser] Parse complete");
  }, "parse"),
  parser: {
    yy: db
  }
};
var diagram = {
  parser,
  db,
  renderer,
  styles: getStyles
};
var railroadDiagram_default = diagram;
export {
  railroadDiagram_default as default,
  diagram
};
//# sourceMappingURL=railroadDiagram-RFXS5EU6-YDHCQDM6.js.map
