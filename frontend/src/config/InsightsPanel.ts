import { msg } from "@lingui/core/macro";

export const InsightsPanel = {
  TITLE: msg`AI Strategic Freight Briefing`,
  STATUS_WARMBOOTING: msg`Warmbooting Session...`,
  STATUS_FETCHING: msg`Fetching Logistics Briefing...`,
  BRAND_FOCUS_PREFIX: msg`Freight Division Focus: `,
  ERROR_MSG: msg`Failed to load dynamic AI Freight Briefings from BigQuery.`,
  EMPTY_MSG_PREFIX: msg`No strategic AI briefings pre-generated for `,
  EMPTY_MSG_SUFFIX: msg` yet.`,
  FOOTER_NOTE: msg`Recommendations generated asynchronously via BigQuery AI for Estes LTL network optimization.`,
  APPLY_BTN: msg`Apply LTL Route Rules`,
  DEFAULT_TITLE: msg`Logistics Strategic Insight`,
  DEFAULT_DESC: msg`No freight briefing details provided.`,
  ALERT_PREFIX: msg`Applied optimal LTL routing and terminal door rules for `,
  ALERT_SUFFIX: msg`. Synchronizing with Looker database...`,
};
