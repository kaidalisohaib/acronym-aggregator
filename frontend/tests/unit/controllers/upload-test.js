import { module, test } from 'qunit';
import { setupTest } from 'frontend/tests/helpers';

module('Unit | Controller | upload', function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test('it exists', function (assert) {
    let controller = this.owner.lookup('controller:authenticated.upload');
    assert.ok(controller);
  });
});
