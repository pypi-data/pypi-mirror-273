from typing import Any, Callable, Dict


class Depends:

    def __init__(self, resolve: Callable, cache_results: bool = True):
        self.resolve = resolve
        self._results = None
        self._cache_results = cache_results

    def __call__(self) -> Any:
        if self._cache_results:
            if self._results is None:
                self._results = self.resolve()
            return self._results
        return self.resolve()


def resolve_create_args(create_args: Dict[str, Any]) -> Dict[str, Any]:
    resolved_args = {}
    for key, item in create_args.items():
        if isinstance(item, Depends):
            resolved_args[key] = item()
        elif isinstance(item, dict):
            resolved_args[key] = resolve_create_args(item)
        else:
            resolved_args[key] = item
    return resolved_args
