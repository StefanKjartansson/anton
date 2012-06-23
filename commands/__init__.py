import events
import traceback
import re
from events import STOP, CONTINUE

COMMANDS = []

def register_raw(fn):
  COMMANDS.append(fn)

def return_callback(callback, result):
  if result is commands.CONTINUE:
    return result

  if result is None or result is commands.STOP:
    pass
  else:
    callback(result)
  return commands.STOP

def re_(r):
  def decorate(fn):
    def new_fn(callback, message):
      m = r.match(message)
      if not m:
        return commands.CONTINUE

      return return_callback(callback, fn(callback, m))

    register_raw(new_fn)
    return new_fn

  return decorate

def command(name, args=-1):
  if isinstance(name, basestring):
    names = set([name])
  else:
    names = set(name)

  def decorate(fn):
    if args == -1:
      args2 = fn.func_code.co_argcount - 1
    else:
      args2 = args

    def new_fn(callback, message):
      tokens = message.split(" ", args2)
      if not tokens[0] in names:
        return commands.CONTINUE

      if args2 > len(tokens) - 1:
        callback("incorrect number of args for command: " + tokens[0])
        return commands.STOP

      return return_callback(callback, fn(callback, *tokens[1:]))

    register_raw(new_fn)
    return new_fn

  return decorate

def all():
  def decorate(fn):
    def new_fn(callback, message):
      return return_callback(callback, fn(callback, message))
    register_raw(new_fn)
    return new_fn
  return decorate

RE_TYPE = type(re.compile(""))
FN_TYPE = type(lambda: None)
def register(*args, **kwargs):
  if not args:
    fn = all
  else:
    first = args[0]
    if isinstance(first, FN_TYPE):
      fn = all()
    elif isinstance(first, RE_TYPE):
      fn = re_
    elif isinstance(first, basestring) or isinstance(first, list):
      fn = command
    else:
      raise Exception("Unknown type for param: %r" % type(first))

  return fn(*args, **kwargs)

@events.register("chanmsg")
def chanmsg_handler(type, irc, obj):
  callback = lambda x: irc.chanmsg(obj["channel"], x)

  try:
    for command in COMMANDS:
      r = command(callback, obj["message"])
      if r == STOP:
        break
  except Exception, e:
    traceback.print_exc()
    callback("exception occured:")
    callback(traceback.format_exc())

@events.register("privmsg")
def privmsg_handler(type, irc, obj):
  callback = lambda x: irc.privnotice(obj["source"]["nick"], x)

  try:
    for command in COMMANDS:
      r = command(callback, obj["message"])
      if r == STOP:
        break
  except Exception, e:
    traceback.print_exc()
    callback("exception occured:\n" + traceback.format_exc())

import commands.learndb
import commands.thanks
import commands.urban_dictionary
import commands.google
import commands.zalgo
import commands.slogan
import commands
