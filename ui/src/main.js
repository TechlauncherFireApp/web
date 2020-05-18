window.DEVICE_IS_MOBILE = new RegExp("Android|webOS|iPhone|iPad|BlackBerry|Windows Phone|Opera Mini|IEMobile|Mobile","i").test(navigator.userAgent);

export const contains = (x) => { return ((x !== undefined) && (x !== null) && (x !== "") && (x.length !== 0)); };

export const getDateSS = (t) => {
    return new Date(t.toString().split("GMT")[0]+" UTC").toISOString().split('.')[0];
};