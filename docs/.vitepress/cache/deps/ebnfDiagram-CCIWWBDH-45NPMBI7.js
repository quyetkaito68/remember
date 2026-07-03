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
import {
  createRailroadEbnfServices
} from "./chunk-2CIAGU4W.js";
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

// node_modules/mermaid/dist/chunks/mermaid.core/ebnfDiagram-CCIWWBDH.mjs
var langiumParser = createRailroadEbnfServices().RailroadEbnf.parser.LangiumParser;
var transformChoice = __name((choice) => {
  const alternatives = choice.alternatives.map(transformSequence);
  if (alternatives.length === 1) {
    return alternatives[0];
  }
  return {
    type: "choice",
    alternatives
  };
}, "transformChoice");
var transformSequence = __name((sequence) => {
  const elements = sequence.elements.map(transformTerm);
  if (elements.length === 1) {
    return elements[0];
  }
  return {
    type: "sequence",
    elements
  };
}, "transformSequence");
var transformPrimary = __name((primary) => {
  switch (primary.$type) {
    case "EbnfTerminal":
      return {
        type: "terminal",
        value: primary.value
      };
    case "EbnfNonTerminal":
      return {
        type: "nonterminal",
        name: primary.name
      };
    case "EbnfSpecial":
      return {
        type: "special",
        text: primary.text
      };
    case "EbnfGroup":
      return transformChoice(primary.element);
    case "EbnfOptional":
      return {
        type: "optional",
        element: transformChoice(primary.element)
      };
    case "EbnfRepetition":
      return {
        type: "repetition",
        element: transformChoice(primary.element),
        min: 0,
        max: Infinity
      };
    default:
      throw new Error(`Unsupported EBNF primary node: ${primary.$type}`);
  }
}, "transformPrimary");
var transformPostfix = __name((node, postfix) => {
  switch (postfix.$type) {
    case "EbnfOptionalPostfix":
      return {
        type: "optional",
        element: node
      };
    case "EbnfZeroOrMorePostfix":
      return {
        type: "repetition",
        element: node,
        min: 0,
        max: Infinity
      };
    case "EbnfOneOrMorePostfix":
      return {
        type: "repetition",
        element: node,
        min: 1,
        max: Infinity
      };
    case "EbnfExceptionPostfix":
      return {
        type: "sequence",
        elements: [
          node,
          { type: "terminal", value: "-" },
          transformPrimary(postfix.except)
        ]
      };
    default:
      throw new Error(`Unsupported EBNF postfix node: ${postfix.$type}`);
  }
}, "transformPostfix");
var transformTerm = __name((term) => {
  return term.postfixes.reduce((currentNode, postfix) => {
    return transformPostfix(currentNode, postfix);
  }, transformPrimary(term.base));
}, "transformTerm");
var transformRule = __name((rule) => {
  return {
    name: rule.name,
    definition: transformChoice(rule.definition)
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
    log.debug("[EBNF Parser] Starting Langium parse");
    const result = langiumParser.parse(input);
    if (result.lexerErrors.length > 0 || result.parserErrors.length > 0) {
      throw new MermaidParseError(result);
    }
    const ast = result.value;
    log.debug("[EBNF Parser] Parsed rules:", ast.rules.length);
    populateDb(ast);
    log.debug("[EBNF Parser] Parse complete");
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
//# sourceMappingURL=ebnfDiagram-CCIWWBDH-45NPMBI7.js.map
