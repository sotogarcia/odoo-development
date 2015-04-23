from pygit2 import clone_repository
from urllib2 import urlopen, Request
import json
from  sys import argv, maxint
from os import path
from getopt import getopt, GetoptError


class EventHook(object):
    # http://www.voidspace.org.uk/python/weblog/arch_d7_2007_02_03.shtml#e616

    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)

    def clearObjectHandlers(self, inObject):
        for theHandler in self.__handlers:
            if theHandler.im_self == inObject:
                self -= theHandler


class Event(object):
    pass


class ErrorEvent(Event):
    message = None

    def __init__(cls, message):
        cls.message = message


class BranchEvent(Event):
    branch = None
    project = None
    url = None
    exists = None

    def exists(self):
        return self._exists

    def __init__(cls, project, branch, url, exists):
        cls.branch = branch
        cls.project = project
        cls.url = url
        cls.exists = exists


class CloneEvent(Event):
    branch = None
    project = None
    cloned = None

    def __init__(cls, project, branch, cloned):
        cls.branch = branch
        cls.project = project
        cls.cloned = cloned


class OCADownloader(object):
    _repos_url = None
    _repos_limit = 0
    onError = None
    onBranch = None

    def __init__(self):
        self._repos_url = 'https://api.github.com/orgs/OCA/repos'
        self._repos_limit = maxint
        self.onError = EventHook()
        self.onBranch = EventHook()
        self.onCloned = EventHook()

    def _json_to_dict(self, json_string):
        result = {}

        if json_string:
            try:
                result = json.loads(json_string)
            except Exception as e:
                error_event = ErrorEvent(e.message)
                self.onError.fire(error_event)

        return result

    def _get_default_branch(self, dict, default='master'):
        branch = default

        if dict and 'default_branch' in dict.keys():
            branch = dict['default_branch']

        return branch

    def _get_branches_url(self, item):
        branches_url = item['branches_url']
        return branches_url.replace('{/branch}', '')

    def _item_is_valid(self, item):
        result = False

        if item and type(item) is dict:
            keys = item.keys()
            result = 'branches_url' in keys and \
                     'name' in keys and \
                     'clone_url' in keys

        return result

    def _branch_exists(self, item, branch, token=None):
        branches_url = self._get_branches_url(item)
        json_string = self.download_json(branches_url, token=token)
        json_list = self._json_to_dict(json_string)

        for item in json_list:
            if 'name' in item.keys() and item['name'] == branch:
                return True  # Exit

        return False

    def get_json_url(self, limit=-1):
        if limit < 0:
            limit = self._repos_limit
        return '{}?per_page={}'.format(self._repos_url, limit)

    def download_json(self, json_url, token=None):
        json_string = '{}'

        try:
            request = Request(json_url)

            if token:
                request.add_header('Authorization', 'token {}'.format(token))

            response = urlopen(request)
            json_string = response.read()
        except Exception as e:
            error_event = ErrorEvent(e.message)
            self.onError.fire(error_event)

        return json_string

    def download_branch(self, required_branch=None, token=None):
        json_url = self.get_json_url()
        json_string = self.download_json(json_url, token)
        json_list = self._json_to_dict(json_string)

        for item in json_list:
            branch = required_branch or self._get_default_branch(item)
            if self._item_is_valid(item) and \
                    self._branch_exists(item, branch, token):

                branch_event = BranchEvent(
                    item['name'], branch, item['clone_url'], True)
                self.onBranch.fire(branch_event)

                cloned = self.clone_project(
                    item['clone_url'], item['name'], branch)

                clone_event = CloneEvent(item['name'], branch, bool(cloned))
                self.onCloned.fire(clone_event)

            else:
                branch_event = BranchEvent(
                    item['name'], branch, item['clone_url'], False)
                self.onBranch.fire(branch_event)

    def clone_project(self, repo_url, repo_path, branch):
        repo = False

        try:
            repo = clone_repository(
                repo_url, repo_path, checkout_branch=branch)

            assert bool(repo), \
                'Unknown error when downloading {}'.format(repo_url)
        except Exception as e:
            error_event = ErrorEvent(e.message)
            self.onError.fire(error_event)

        return repo

def onError(event):
    print event.message


def onBranch(event):
    if event.exists:
        print('{} ({}): {}'.format(event.project, event.branch, event.url))
    else:
        print('There is not branch {} for {}'.format(
            event.branch, event.project))


def onCloned(event):
    if event.cloned:
        print('Branch {} from repository {} have been cloned'.format(
            event.branch, event.project))

od = OCADownloader()
od.onError += onError
od.onBranch += onBranch
od.onCloned += onCloned

branch = 'master'
token = False

try:
    optlist, args = getopt(
        argv[1:], ':bth:', ['branch=', 'token=', 'help'])
    for arg, value in optlist:
        if arg in ('-h', '--help'):
            app_path = path.split(argv[0])[-1]
            msg = u'{} [--branch=branch] [--token=token] [--help]'
            print(msg.format(app_path))
            exit(0)
        elif arg in ('-b', '--branch'):
            branch = value
        elif arg in ('-t', '--token'):
            token = value
        else:
            print (u'Invalid argument ({})'.format(arg))
except GetoptError as error:
    print u'ERROR: {}'.format(error)

od.download_branch(required_branch=branch, token=token)
