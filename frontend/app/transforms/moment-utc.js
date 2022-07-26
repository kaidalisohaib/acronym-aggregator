import Transform from '@ember-data/serializer/transform';
import moment from 'moment';
/**
 * This transform is to set everything in UTC time.
 */
export default class MomentUTCTransform extends Transform {
  deserialize(serialized) {
    return serialized
      ? moment.utc(serialized).format('YYYY-MM-DDTHH:mm:ss.SSS')
      : null;
  }

  serialize(deserialized) {
    return deserialized
      ? moment.utc(deserialized).format('YYYY-MM-DDTHH:mm:ss.SSS')
      : null;
  }
}
