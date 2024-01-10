const BASE_API_URL = 'http://localhost:8000'

const get_token = () => {
    let token = localStorage.getItem('token')
    let res = ''
    if (token) {
        res = 'JWT ' + token
    }
    return (
        res
    )
}

export class BaseAPI {
    constructor({ endpoint }) {
        this._url = BASE_API_URL + '/' + endpoint;
        this._token = get_token()
        this._headers = {
            'Content-Type': 'application/json',
            Authorization: this._token
        };
    }

    async getData() {
        try {
            const response = await fetch(`${this._url}`, {
                mode: 'cors',
                method: 'GET',
                headers: this._headers
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async postData(data) {
        try {
            const response = await fetch(`${this._url}`, {
                mode: 'cors',
                method: 'POST',
                headers: this._headers,
                body: JSON.stringify(data)
            });
            const responseData = await response.json();
            return responseData;
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async patchData(id, data) {
        try {
            const response = await fetch(`${this._url}/${id}`, {
                method: 'PATCH',
                headers: this._headers,
                body: JSON.stringify(data)
            });
            const responseData = await response.json();
            return responseData;
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async putData(id, data) {
        try {
            const response = await fetch(`${this._url}/${id}`, {
                method: 'PUT',
                headers: this._headers,
                body: JSON.stringify(data)
            });
            const responseData = await response.json();
            return responseData;
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async deleteData(id) {
        try {
            const response = await fetch(`${this._url}/${id}`, {
                method: 'DELETE',
                headers: this._headers,
            });
            const responseData = await response.json();
            return responseData;
        } catch (error) {
            console.error('Error:', error);
        }
    }
}
