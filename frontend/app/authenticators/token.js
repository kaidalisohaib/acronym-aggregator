import Base from 'ember-simple-auth/authenticators/base';

export default Base.extend({
  async restore(data) {
    let { access_token } = data;
    if (access_token) {
      return data;
    }
    throw new Error('No valid session data');
  },

  async authenticate(email, password) {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      return response.json();
    }

    let errors;
    await response.json().then((errorsData) => {
      errors = errorsData;
    });
    throw errors;
  },

  async invalidate(/* data */) {
    try {
      localStorage.removeItem('access_token');
      return true;
    } catch {
      throw new Error('Failed to logout.');
    }
  },
});
