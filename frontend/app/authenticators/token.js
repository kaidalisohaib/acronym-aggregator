import Base from 'ember-simple-auth/authenticators/base';

export default Base.extend({
  /**
   *
   * @param {*} data
   * @returns If the old authentication data is found in the session store
   * we restore it.
   */
  async restore(data) {
    let { access_token } = data;
    if (access_token) {
      return data;
    }
    throw new Error('No valid session data');
  },

  /**
   * Try to authenticate/login the user with the email and password
   * via the backend api.
   * @param {string} email
   * @param {string} password
   * @returns The response json.
   */
  async authenticate(email, password) {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    // If the response if good return the json.
    if (response.ok) {
      return response.json();
    }

    // If the response return an error, throw the error
    // from the json.
    let errors;
    await response.json().then((errorsData) => {
      errors = errorsData;
    });
    throw errors;
  },

  /**
   * Try to invalidate/logout by removing the JWT token
   * from the session store.
   * @returns True if success, otherwise false.
   */
  async invalidate(/* data */) {
    try {
      localStorage.removeItem('access_token');
      return true;
    } catch {
      throw new Error('Failed to logout.');
    }
  },
});
