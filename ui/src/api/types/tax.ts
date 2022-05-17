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
  cgst: number;
  total: number;
  active: boolean;
  issued_on: string;
  salary_income: number;
  share_market_income: number;
  transaction_type: TransactionType;
};

export type Tax = {
  id: number;
  sgst: number;
  paid: boolean;
  due_date: string;
  status: StatusType;
  updated_on: string;
  payer: string | number;
  history?: TaxDueInfo[];
  active_due: TaxDueInfo;
};

export type CreateUpdateTaxData = {
  id?: number;
  payer: number;
  due_date: string;
  payer_name?: string;
  history?: TaxDueInfo[];
  active_due: {
    cgst: number;
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
