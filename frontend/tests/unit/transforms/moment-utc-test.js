import { module, test } from 'qunit';
import { setupTest } from 'frontend/tests/helpers';

module('Unit | Transform | moment utc', function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test('it exists', function (assert) {
    let transform = this.owner.lookup('transform:moment-utc');
    assert.ok(transform);
  });
});
