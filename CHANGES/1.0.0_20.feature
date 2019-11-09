[BREAKING CHANGE] - This change won't be compatible with old version of library.
  Middleware refactoring.
  Now `post_process_event` accepts the new argument `result` which is result of handler work (if handler return `False` handler will be skipped and `Dispatcher` will try process next handler, be careful.)
  `pre_process_event` accepts not a raw dict, it accepts a completely pydantic object.