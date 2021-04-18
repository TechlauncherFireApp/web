export const att = (s, b) => {
  if (b !== undefined && b === false) return {};
  return { [s]: '' };
};

export const contains = (...y) => {
  for (const x of y)
    if (
      x === undefined ||
      x === null ||
      x === '' ||
      x.length === 0 ||
      (typeof x === 'number' && isNaN(x))
    )
      return false;
  return true;
};

export const toTimeblock = (d) => {
  if (!contains(d)) return 0; // d === "Invalid Date"
  return d.getDay() * 48 + d.getHours() * 2 + (d.getMinutes() === 0 ? 0 : 1);
};

export const getValidDate = (x) => {
  x.setMilliseconds(0);
  x.setSeconds(0);
  x.setMinutes(x.getMinutes() >= 30 ? 30 : 0);
  return x;
};

export const getDateSS = (t) => {
  return new Date(t.toString().split('GMT')[0] + ' UTC')
    .toISOString()
    .split('.')[0];
};

export const toPythonDate = (d) => {
  return d.toISOString();
};

export const dateToBackend = (d) => {
  let month = `${d.getMonth() + 1}`;
  if (month.length === 1) month = '0' + month;
  let date = `${d.getDate()}`;
  if (date.length === 1) date = '0' + date;
  return `${d.getFullYear()}-${month}-${date}T${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}.${d
    .getMilliseconds()
    .toString()}`;
};

export const dateFromBackend = (d) => {
  return new Date(Date.parse(d.split('.')[0]));
};

export const makeid = (l = 15) => {
  let r = '';
  const c = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  for (let i = 0; i < l; i++)
    r += c.charAt(Math.floor(Math.random() * c.length));
  return r;
};

// handles display of date/time info
export const parseDateTime = (date1, date2) => {
  let str = date1.toLocaleDateString('en-GB');
  if (
    date1.getMonth() === date2.getMonth() &&
    date1.getDate() === date2.getDate() &&
    date1.getFullYear() === date2.getFullYear()
  ) {
    //if the request starts and ends on the same day
    str =
      str +
      ' ' +
      date1.toLocaleTimeString('en-US', {
        hour12: true,
        hour: 'numeric',
        minute: 'numeric',
      }) +
      ' - ' +
      date2.toLocaleTimeString('en-US', {
        hour12: true,
        hour: 'numeric',
        minute: 'numeric',
      });
  } else {
    str =
      str +
      ' ' +
      date1.toLocaleTimeString('en-US', {
        hour12: true,
        hour: 'numeric',
        minute: 'numeric',
      }) +
      ' - ' +
      date2.toLocaleDateString('en-GB') +
      ' ' +
      date2.toLocaleTimeString('en-US', {
        hour12: true,
        hour: 'numeric',
        minute: 'numeric',
      });
  }
  return str.toLowerCase();
};

export const parseRolesAsString = (list) => {
  let s = '';
  for (const l of list) {
    s += toSentenceCase(l) + '/';
  }
  return s.slice(0, -1);
};

export const isAvailable = (availability, shift) => {
  for (let i = 0; i < availability.length; i++) {
    if (
      availability[i].startTime <= shift.startTime &&
      availability[i].endTime >= shift.endTime
    ) {
      return true;
    }
  }
  return false;
};

export const toSentenceCase = (camelCase) => {
  const result = camelCase.replace(/([A-Z])/g, ' $1');
  return result.charAt(0).toUpperCase() + result.slice(1);
};
