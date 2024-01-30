export const defHeaders = { 'Content-Type': 'application/json' };
export const loginURL = "http://127.0.0.1:8000/auth/login";
export const instanceURL = "http://127.0.0.1:8000";

export async function EasyRequest(url, headers, method, body=null) {
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
        return { data: error, status: 500 };
    }

}


// const url = "http://127.0.0.1:8000/auth/login/";
// const headers = { 'Content-Type': 'application/json' };
// const method = "POST";
// const body = { "email": "test", "password": "testtest" };

// const test = await EasyRequest(url, headers, method, body).then(val => console.log(val));

// console.log(test)