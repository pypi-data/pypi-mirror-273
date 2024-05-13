"""Subclass of QThread allowing for the running instance of App to
gracefully handle the threads. """
#  GPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable, Any, TYPE_CHECKING

from PySide6.QtCore import QThread, Slot, Signal
from icecream import ic
from vistutils.waitaminute import typeMsg
from ezside.app import AppSettings

if TYPE_CHECKING:
  pass


class AppThread(QThread):
  """Subclass of QThread allowing for the running instance of App to
  gracefully handle the threads. """

  __termination_flag__ = None
  __paused_flag__ = None
  __loop_time__ = None
  __fallback_time__ = 250
  __callback_funcs__ = None

  quitInitiated = Signal()

  loopStarted = Signal()
  loop = Signal()
  loopEnded = Signal()

  callbackError = Signal(Exception)
  callbackLoop = Signal(object)
  callbackExit = Signal()

  normalExit = Signal()
  normalTimeout = Signal()
  quitExit = Signal()
  quitTimeout = Signal()
  terminateExit = Signal()
  terminateTimeout = Signal()

  def __init__(self, *args, **kwargs) -> None:
    """Initialize the AppThread."""
    self.__termination_flag__ = False
    self.__paused_flag__ = False
    QThread.__init__(self, *args, **kwargs)
    self.quitInitiated.connect(self._activateTerminationFlag)
    self.normalExit.connect(lambda: ic('Normal exit'))
    self.normalTimeout.connect(lambda: ic('Normal timeout'))
    self.quitExit.connect(lambda: ic('Quit exit'))
    self.quitTimeout.connect(lambda: ic('Quit timeout'))
    self.terminateExit.connect(lambda: ic('Terminate exit'))
    self.terminateTimeout.connect(lambda: ic('Terminate timeout'))

  def setTime(self, loopTime: int) -> None:
    """Set the loop time."""
    if not isinstance(loopTime, int):
      e = typeMsg('loopTime', loopTime, int)
      raise TypeError(e)
    self.__loop_time__ = loopTime

  def getTime(self, ) -> int:
    """Get the loop time."""
    if self.__loop_time__ is None:
      return self.__fallback_time__
    return self.__loop_time__

  def setCallbacks(self, *callMeMaybe: Callable) -> None:
    """Set the callbacks."""
    if self.__callback_funcs__ is None:
      self.__callback_funcs__ = []
    for callback in callMeMaybe:
      if callable(callback):
        self.__callback_funcs__.append(callback)
      else:
        e = typeMsg('callback', callback, Callable)
        raise TypeError(e)
    else:
      self.__callback_funcs__.append(self.loop.emit)

  def getCallbacks(self, **kwargs) -> list[Callable]:
    """Get the callbacks."""
    if self.__callback_funcs__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self.setCallbacks()
      return self.getCallbacks(_recursion=True)
    return self.__callback_funcs__

  @Slot()
  def requestQuit(self) -> None:
    """This slot informs the thread to begin shutdown procedure. Please
    note that this method implements substantial opportunity for error
    handling that should allow the system to gracefully exit. If the
    system fails to intervene however, the thread will eventually raise
    SystemExit. """
    self.quitInitiated.emit()
    settings = AppSettings()
    normalExitTime = settings.value('thread/normal_exit_time', 5000)
    quitExitTime = settings.value('thread/quit_exit_time', 5000)
    terminateExitTime = settings.value('thread/terminate_exit_time', 5000)
    if self.wait(normalExitTime):
      return self.normalExit.emit()
    self.normalTimeout.emit()
    self.quit()
    if self.wait(quitExitTime):
      return self.quitExit.emit()
    self.quitTimeout.emit()
    self.terminate()
    if self.wait(terminateExitTime):
      return self.terminateExit.emit()
    self.terminateTimeout.emit()
    raise SystemExit  # This state should be prevented by the application.

  @Slot()
  def pause(self, ) -> None:
    """Pause the thread."""
    self._setPausedFlag(True)

  @Slot()
  def resume(self, ) -> None:
    """Resume the thread."""
    self._setPausedFlag(False)

  def _getTermFlag(self, **kwargs) -> bool:
    """Get the termination flag."""
    return True if self.__termination_flag__ else False

  def _setTermFlag(self, value: bool) -> None:
    """Set the termination flag."""
    self.__termination_flag__ = True if value else False

  @Slot()
  def _deactivateTerminationFlag(self) -> None:
    """Deactivate the termination flag."""
    self.__termination_flag__ = False

  @Slot()
  def _activateTerminationFlag(self) -> None:
    """Activate the termination flag."""
    self.__termination_flag__ = True

  def _getPausedFlag(self) -> bool:
    """Get the paused flag."""
    return True if self.__paused_flag__ else False

  def _setPausedFlag(self, value: bool) -> None:
    """Set the paused flag."""
    self.__paused_flag__ = True if value else False

  def start(self, *args, ) -> Any:
    """Start the thread."""
    self.__termination_flag__ = False
    return QThread.start(self, *args)

  def run(self) -> None:
    """Until quit is requested, the thread will run each of its callback
    functions in the defined order. Any exceptions raised during a
    callback is emitted through the callbackError signal which causes a
    premature exit of the loop following by the callbackLoop signal
    informing about the callable reached when the error was caught.
    Finally, the callbackExit signal is emitted.

    If instead the thread receives a request to quit, it will finish the
    current while loop and emit the loopEnded signal, instead of starting
    a new loop. """

    self.loopStarted.emit()
    loopTime = self.getTime()
    callbacks = self.getCallbacks()
    callMeMaybe = None
    while not self._getTermFlag():
      self.msleep(loopTime)
      if self._getPausedFlag():
        continue
      for callMeMaybe in callbacks:
        try:
          callMeMaybe()
        except Exception as exception:
          self.callbackError.emit(exception)
          break
      else:
        continue
      break
    else:
      return self.loopEnded.emit()
    self.callbackLoop.emit(callMeMaybe)
    self.callbackExit.emit()
