import objc as _objc
# this can be an absolute path too
_path = _objc.pathForFramework('DiscRecording.framework')
_objc.loadBundle(
    'DiscRecording', globals(), bundle_path=_path)
