export const defHeaders = { 'Content-Type': 'application/json' };
export const loginURL = "http://127.0.0.1:5000/login";
export const instanceURL = "http://127.0.0.1";

export async function EasyRequest(url = "127.0.0.1:5000",
    headers = { 'Content-Type': 'application/json' }, method = "GET", body = false) {

    try {
        let options = '';
        if (body) {
            options = {
                method: method,
                headers: headers,
                body: JSON.stringify(body)
            };
        } else {
            options = {
                method: method,
                headers: headers,
            };
        }

        const req = await fetch(url, options);
        const res_data = await req.json();

        return { data: res_data, status: req.status };

    } catch (error) {
        console.log(`An ERROR: --> ${error}`);
    }

}


// const url = "http://127.0.0.1:5000/login";
// const headers = { 'Content-Type': 'application/json' };
// const method = "POST";
// const body = { "username": "test", "password": "testtest" };

// test = EasyRequest(url, headers, method, body).then(val => console.log(val));

// console.log(test)