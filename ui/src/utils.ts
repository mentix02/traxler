export const formatTaxpayerName = (taxpayer: string | number) => {
  let fmtName = taxpayer.toString();
  const idx = fmtName.indexOf("-");
  if (idx !== -1) return fmtName.substring(0, idx - 1);
  return fmtName;
};
