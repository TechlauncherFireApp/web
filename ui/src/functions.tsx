export const contains = (...y: any): boolean => {
  for (let x of y) if (
    (x === undefined) || (x === null) ||
    (x === "") || (x.length === 0) ||
    ((typeof x === "number") && isNaN(x))
  ) return false;
  return true;
};

export const toTimeblock = (d: Date): (Number | Date) => {
  if (!contains(d)) return 0; // d === "Invalid Date"
  return d.getDay() * 48 + d.getHours() * 2 + (d.getMinutes() === 0 ? 0 : 1);
};

export const getValidDate = (x: Date): Date => {
  x.setMilliseconds(0);
  x.setSeconds(0);
  x.setMinutes(x.getMinutes() >= 30 ? 30 : 0);
  return x;
}

export const getDateSS = (t: Date): string => { return new Date(t.toString().split("GMT")[0] + " UTC").toISOString().split('.')[0]; };

export const toPythonDate = (d: Date): string => {
  return (`${d.getFullYear()}-${(d.getMonth() + 1)}-${d.getDate()} ${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}.${d.getMilliseconds().toString()}`);
};

export const makeid = (): string => {
  let r: string = "",
    c: string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
    l: number = 15;
  for (let i = 0; i < l; i++) r += c.charAt(Math.floor(Math.random() * c.length));
  return r;
}

// handles display of date/time info
export const parseDateTime = (date1: Date, date2: Date): string => {
  let str = date1.toLocaleTimeString("en-US", { hour12: true, hour: "numeric", minute: "numeric" });
  if (
    date1.getMonth() === date2.getMonth() &&
    date1.getDate() === date2.getDate() &&
    date1.getFullYear() === date2.getFullYear()
  ) {
    //if the request starts and ends on the same day
    str = str + " - " + date2.toLocaleTimeString("en-US", { hour12: true, hour: "numeric", minute: "numeric" }) + " "
      + date2.toLocaleDateString("en-GB");
  } else {
    str = str + " " + date1.toLocaleDateString("en-GB") + " - "
      + date2.toLocaleTimeString("en-US", { hour12: true, hour: "numeric", minute: "numeric" }) + " "
      + date2.toLocaleDateString("en-GB");
  }
  return str.toLowerCase();
};