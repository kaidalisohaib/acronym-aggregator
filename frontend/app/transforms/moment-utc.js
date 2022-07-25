import Transform from '@ember-data/serializer/transform';
import moment from 'moment';
export default class MomentUTCTransform extends Transform {
  deserialize(serialized) {
    return serialized ? moment.utc(serialized) : null;
  }

  serialize(deserialized) {
    return deserialized ? moment.utc(deserialized).format() : null;
  }
}
