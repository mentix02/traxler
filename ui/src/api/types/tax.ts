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

export type TaxDueInfo = {
  cgst: number;
  total: number;
  active: boolean;
  due_date: string;
  issued_on: string;
  salary_income: number;
  share_market_income: number;
  transaction_type: TransactionType;
};

export type Tax = {
  id: number;
  sgst: number;
  paid: boolean;
  status: StatusType;
  updated_on: string;
  payer: string | number;
  history?: TaxDueInfo[];
  active_due: TaxDueInfo;
};

export type CreateUpdateTaxData = {
  id?: number;
  payer: number;
  payer_name?: string;
  history?: TaxDueInfo[];
  active_due: {
    cgst: number;
    due_date: string;
    salary_income: number;
    share_market_income: number;
    transaction_type: TransactionType;
  };
};

export type State = {
  id: number;
  tax: number;
  name: string;
};
