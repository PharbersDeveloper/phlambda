import R = require("ramda")
import { FinalizedOperatorDesc, OperatorDesc, ParserOperatorsConfig } from "../../types"
import { isFieldExpression, isId } from "./parse-query-params"

export const ASSUMED_BINARY_OPERATORS =
  ["eq", "neq", "ne", "in", "nin", "lt", "gt", "lte", "gte"]

export function finalizeOperatorConfig(
  assumedBinaryOps: string[],
  operatorName: string,
  operatorConfig: OperatorDesc
): FinalizedOperatorDesc {
  // Set defaults for legalIn, arity, and finalizeArgs on every operator.
  const {
    legalIn = ["filter"] as Array<"filter">,
    arity = assumedBinaryOps.includes(operatorName) ? 2 : Infinity,
    finalizeArgs = finalizeFilterFieldExprArgs
  } = operatorConfig

  return { ...operatorConfig, legalIn, arity, finalizeArgs }
}

export default R.partial(finalizeOperatorConfig, [ASSUMED_BINARY_OPERATORS])

/**
 * A default function called to finalize the arguments of a given
 * field expression. This function enforces a number of invariants to simplify
 * the process of writing a correct adapter, but adapters that want looser
 * constraints on operator values can replace it with their own function.
 * In particular it: 1) requires that `and` and `or` operators take a non-empty
 * list of field expressions as their arguments; and 2) requires that binary
 * operators have an identifier as their first argument and a plain value (i.e.,
 * one with no identifiers) as their second.
 */
export function finalizeFilterFieldExprArgs(
  conf: ParserOperatorsConfig,
  operator: string,
  args: any[]
) {
  if (operator === "and" || operator === "or") {
    if (args.length === 0) {
      throw new Error(`The "${operator}" operator requires at least one argument.`)
    }

    if (!args.every(isFieldExpression)) {
      throw new Error(
        `The "${operator}" operator expects its arguments to be field expressions.`
      )
    }
  } else if (conf[operator]!.arity === 2) {
    if (!isId(args[0])) {
      throw new SyntaxError(
        `"${operator}" operator expects field reference as first argument.`
      )
    }

    try {
      assertNoIdentifiers(args[1])
    } catch (e) {
      throw new SyntaxError(
        `Identifier not allowed in second argument to "${operator}" operator.`
      )
    }
  } else if (conf[operator]!.arity !== Infinity && args.length !== conf[operator]!.arity) {
    throw new SyntaxError(
      // tslint:disable-next-line no-non-null-assertion
      `"${operator}" operator expects exactly ${conf[operator]!.arity} arguments; got ${args.length}.`
    )
  }

  return args
}

function assertNoIdentifiers(it: any) {
  if (Array.isArray(it)) {
    it.forEach(assertNoIdentifiers)
  }

  if (isId(it)) {
    throw new Error("Identifier not allowed in this context.")
  }
}
