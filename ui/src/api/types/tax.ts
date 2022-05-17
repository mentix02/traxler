export const INTERSTATE_TRANSACTION = true;
export const INTRASTATE_TRANSACTION = false;

type TransactionType =
  | typeof INTERSTATE_TRANSACTION
  | typeof INTRASTATE_TRANSACTION;

export const STATUS_NEW = "New";
export const STATUS_PAID = "Paid";
export const STATUS_DELAYED = "Delayed";

export type StatusType =
  | typeof STATUS_PAID
  | typeof STATUS_NEW
  | typeof STATUS_DELAYED;

type TaxDueInfo = {
  total: number;
  active: boolean;
  issued_on: string;
  salary_income: number;
  share_market_income: number;
};

export type Tax = {
  id: number;
  cgst: number;
  sgst: number;
  paid: boolean;
  due_date: string;
  status: StatusType;
  updated_on: string;
  payer: string | number;
  history?: TaxDueInfo[];
  active_due: TaxDueInfo;
  transaction_type: TransactionType;
};

export type CreateUpdateTaxData = {
  cgst: number;
  payer: number;
  due_date: string;
  transaction_type: TransactionType;
  active_due: {
    salary_income: number;
    share_market_income: number;
  };
};
