window.DEVICE_IS_MOBILE = new RegExp("Android|webOS|iPhone|iPad|BlackBerry|Windows Phone|Opera Mini|IEMobile|Mobile","i").test(navigator.userAgent);

export const contains = (x) => { return ((x !== undefined) && (x !== null) && (x !== "") && (x.length !== 0)); }

export const Index_In_Parent = (e) => {
    let n = e.parentNode.children;
    for (let i=0;i<n.length;i++) if (n[i] === e) return i;
    return null;
}

// Date.prototype.Now = () => {
//     let x = new Date(),
//         microseconds = Math.floor(Math.random() * 10).toString() + Math.floor(Math.random() * 10).toString() + Math.floor(Math.random() * 10).toString();
//     return (x.getFullYear() + "-" + (x.getMonth()+1) + "-" + x.getDate() + " "
//             + x.getHours() + ":" + x.getMinutes() + ":" + x.getSeconds() + "." + microseconds + x.getMilliseconds().toString());
// };

// Array.prototype.Remove_Item = function(e) {
//     for (let i=0;i<this.length;i++) if (this[i] === e) { this.splice(i, 1); return; }
// };

// /*
//     ----------------------------------------------------------------------------------------------------
//     ---------------------------------------------- COMPONENTS ------------------------------------------
//     ----------------------------------------------------------------------------------------------------
// */

// // SELECT
// HTMLSelectElement.prototype.Set_Option = function(option) {
//     let y = Array.prototype.slice.call(this.querySelectorAll("option"));
//     for (let x=0;x<y.length;x++) if (y[x].value === option) { y[x].selected = true; return; }
//     this.selectedIndex = -1;
// };