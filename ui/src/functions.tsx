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
  x.setMilliseconds(0);
  x.setSeconds(0);
  x.setMinutes(x.getMinutes() >= 30 ? 30 : 0);
  return x;
}

export const getDateSS = (t: Date): string => { return new Date(t.toString().split("GMT")[0]+" UTC").toISOString().split('.')[0]; };

export const toPythonDate = (d: Date): string => {
  return (`${d.getFullYear()}-${(d.getMonth()+1)}-${d.getDate()} ${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}.${d.getMilliseconds().toString()}`);
};

export const makeid = (): string => {
  let result     : string = "",
      characters : string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
      length     : number = 15;
  for (let i = 0; i < length; i++) result += characters.charAt(Math.floor(Math.random() * characters.length));   
  return result;
}