type TaxPayerInfo = {
  pan: string;
  gstin: string;
  state: string;
  address: string;
  business_name: string;
};

export type TaxPayer = {
  id: number;
  email: string;
  username: string;
  last_name: string;
  first_name: string;
  paid_taxes: number;
  total_taxes: number;
  info: TaxPayerInfo;
  date_joined: string;
};

export type TaxpayerUsernameId = {
  id: number;
  username: string;
};
