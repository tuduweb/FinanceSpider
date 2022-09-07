#!/bin/python3
#Coding="utf-8"

from base64 import encode
import encodings
import sys
import os
import datetime
import json
import github
from github import Github

class GitIssueProxy(object):
    pass

class dataSaver(object):
    def __init__(self, GitApi, date):
        print(GitApi)
        self.DebugMode = False
        self.__gitApi = GitApi
        self.g = Github(GitApi)
        self.repo = self.g.get_repo("tuduweb/FinanceSpider")
        self.timezone = datetime.timezone(datetime.timedelta(hours=+0))
        pass

    def _checkValidation(self):
        # 权限验证.. 在初始化的时候如果没有权限那么报错.
        pass

    # 根据日期查看是否存在...
    def _getIssueItemByDate(self, date):
        # https://api.github.com/repos/tuduweb/FinanceSpider/issues?labels=daily&milestone=1&sort=create&direction=desc&since=
        issueItem = None
        result = False
        print("date type:", type(date))
        if isinstance(date, datetime.datetime) is False:
            print("isinstance date is False")
            return False, None
        
        print("in date", date)
        print("cal date", date - datetime.timedelta(hours=date.hour, minutes=date.minute, seconds=date.second, microseconds=date.microsecond))
        
        todayDate = date - datetime.timedelta(hours=date.hour, minutes=date.minute, seconds=date.second, microseconds=date.microsecond)
        since = todayDate.astimezone(self.timezone)
        print("search issue since:", since)
        issues = self.repo.get_issues(labels=['daily'], since=since)

        for iss in issues:
            print("issues", iss.labels)
        
        issuesList = issues.get_page(0)

        # 查看长度，选取最头的那个作为database
        if len(issuesList):
            result = True
            issueItem = issuesList[0]
        
        return result, issueItem

    def _commentOnIssueItem(self, issueItem, comment):
        _commentString = ""
        if isinstance(comment, str):
            _commentString = comment
        elif isinstance(comment, object):
            _commentString = json.dumps(comment) # "test %s" % datetime.datetime.now()
        
        if len(_commentString) is False:
            return

        res = issueItem.create_comment(_commentString)
        print(res)
        pass
    
    def _getAllcommentsInIssue(self, issueId):
        issue = self.repo.get_issue(issueId)
        print(issue.get_comments())
        for comment in issue.get_comments():
            print(comment.body)
        pass


    # def _createNewIssue(self, **kwargs):        
    #     pass

    def _createNewIssue(self, title, body):
        # , assignee="github-username"
        return self.repo.create_issue(title = title,
            body = body,
            labels = [self.repo.get_label("daily")],
            milestone = self.repo.get_milestone(number = 1)
            )
        pass

    def _saveDataItem(self, date, content):
        # find Valid issue by the date
        res, issueItem = self._getIssueItemByDate(date)

        print("item", issueItem)

        if res is False:
            # create a new Issue
            print("should create new issue")

            # temp. todo: from template class
            _title = date.strftime("%Y-%m-%d") + " database"
            _content = "[config content]"
            
            issueItem = self._createNewIssue(_title, _content)
            if issueItem is None:
                print("cant create a new issue")
                return

        # print(issueItem)

        # create comments
        self._commentOnIssueItem(issueItem, content)
        pass

    pass

if __name__ == "__main__":

    GITHUB_API_KEY = sys.argv[1]
    argv2 = sys.argv[2]

    path = ""
    commentString = ""

    # 根据argv2的内容自适应时文件还是内容
    if argv2:
        if os.path.exists(argv2):
            path = argv2
            with open(path, "r") as f: #encoding="UTF-8"
                res = f.read()
                print("content to write", res)
                commentString = res
        else:
            commentString = argv2
    
    date = "2022-10-11"
    print("comments", commentString)

    saver = dataSaver(GITHUB_API_KEY, date)
    
    # res, issueItem = saver._getIssueItemByDate(123)
    # if res:
    #     if len(path):
    #         with open(path, "r") as commentFile:
    #             commentString = json.load(commentFile)
    
    #     saver._commentOnIssueItem(issueItem, commentString)

    # saver._createNewIssue("biaoti222", "content")
    saver._saveDataItem(datetime.datetime.today(), commentString)
    # saver._getAllcommentsInIssue(1)