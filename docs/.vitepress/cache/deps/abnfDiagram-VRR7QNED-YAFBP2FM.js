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
import "./chunk-UFHR6W3S.js";
import "./chunk-2CIAGU4W.js";
import {
  createRailroadAbnfServices
} from "./chunk-AK6KVMQY.js";
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

// node_modules/mermaid/dist/chunks/mermaid.core/abnfDiagram-VRR7QNED.mjs
var langiumParser = createRailroadAbnfServices().RailroadAbnf.parser.LangiumParser;
var transformAlternation = __name((alt) => {
  const alternatives = alt.alternatives.map(transformConcatenation);
  if (alternatives.length === 1) {
    return alternatives[0];
  }
  return {
    type: "choice",
    alternatives
  };
}, "transformAlternation");
var transformConcatenation = __name((concat) => {
  const elements = concat.elements.map(transformElement);
  if (elements.length === 1) {
    return elements[0];
  }
  return {
    type: "sequence",
    elements
  };
}, "transformConcatenation");
var parseRepeat = __name((repeat) => {
  if (repeat.includes("*")) {
    const [minStr, maxStr] = repeat.split("*");
    const min = minStr ? parseInt(minStr, 10) : 0;
    const max = maxStr ? parseInt(maxStr, 10) : Infinity;
    return { min, max };
  }
  const exact = parseInt(repeat, 10);
  return { min: exact, max: exact };
}, "parseRepeat");
var transformElement = __name((element) => {
  const inner = transformPrimary(element.primary);
  if (!element.repeat) {
    return inner;
  }
  const { min, max } = parseRepeat(element.repeat);
  if (min === 0 && max === 1) {
    return { type: "optional", element: inner };
  }
  return {
    type: "repetition",
    element: inner,
    min,
    max
  };
}, "transformElement");
var transformPrimary = __name((primary) => {
  switch (primary.$type) {
    case "AbnfStringLiteral":
      return {
        type: "terminal",
        value: primary.value
      };
    case "AbnfNumVal":
      return {
        type: "terminal",
        value: primary.value
      };
    case "AbnfRuleName":
      return {
        type: "nonterminal",
        name: primary.name
      };
    case "AbnfGroup":
      return transformAlternation(primary.element);
    case "AbnfOptionalGroup":
      return {
        type: "optional",
        element: transformAlternation(primary.element)
      };
    default:
      throw new Error(`Unsupported ABNF primary node: ${primary.$type}`);
  }
}, "transformPrimary");
var transformRule = __name((rule) => {
  return {
    name: rule.name,
    definition: transformAlternation(rule.definition)
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
    log.debug("[ABNF Parser] Starting Langium parse");
    const result = langiumParser.parse(input);
    if (result.lexerErrors.length > 0 || result.parserErrors.length > 0) {
      throw new MermaidParseError(result);
    }
    const ast = result.value;
    log.debug("[ABNF Parser] Parsed rules:", ast.rules.length);
    populateDb(ast);
    log.debug("[ABNF Parser] Parse complete");
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
export {
  diagram
};
//# sourceMappingURL=abnfDiagram-VRR7QNED-YAFBP2FM.js.map
