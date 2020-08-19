export const contains = (...y: any): boolean => {
  for (let x of y) if (
    (x === undefined) || (x === null) ||
    (x === "") || (x.length === 0) ||
    ((typeof x === "number") && isNaN(x))
  ) return false;
  return true;
};

export const toTimeblock = (d: Date) => {
  if (!contains(d)) return 0; // d === "Invalid Date"
  return d.getDay() * 48 + d.getHours() * 2 + (d.getMinutes() === 0 ? 0 : 1);
};

export const getValidDate = (x: Date): Date => {
  x.setSeconds(0);
  x.setMinutes(x.getMinutes() >= 30 ? 30 : 0);
  return x;
}

export const getDateSS = (t: Date): string => { return new Date(t.toString().split("GMT")[0]+" UTC").toISOString().split('.')[0]; };