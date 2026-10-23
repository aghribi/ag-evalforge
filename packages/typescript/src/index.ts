export type { EvalCase, EvalResult, EvalReport } from "./models";
export { makeCase, reportSummary, meanScore, passRate, filterDataset } from "./models";
export { runEval, compare } from "./runner";
export type { ModelFn, RunOptions } from "./runner";
export { ExactMatchScorer, RegexScorer, RougeScorer, rougeL, LLMJudgeScorer, CustomScorer, HostedScorer } from "./scorers";
export type { Scorer, HostedScorerOptions } from "./scorers";
export { load as loadDataset, fromJSON, fromJSONL, fromCSV } from "./datasets/loaders";

// Read at runtime so the exported version always matches the published package.
export const VERSION: string = require("../package.json").version;
