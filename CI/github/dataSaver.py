#!/bin/python3
#Coding="utf-8"

import sys
import datetime
import json
import github
from github import Github

class GitIssueProxy(object):
    pass

class dataSaver(object):
    def __init__(self, GitApi, date):
        print(GitApi)
        self.__gitApi = GitApi
        self.g = Github(GitApi)
        self.repo = self.g.get_repo("tuduweb/FinanceSpider")
        pass

    # 根据日期查看是否存在...
    def _getIssueItemByDate(self, date):
        # https://api.github.com/repos/tuduweb/FinanceSpider/issues?labels=daily&milestone=1&sort=create&direction=desc&since=
        issueItem = None
        result = False
        
        repo = self.g.get_repo("tuduweb/FinanceSpider")
        since=datetime.datetime(2021, 10, 20)
        print(since)
        issues = repo.get_issues(labels=['daily'], since=since)
        print(issues)
        for iss in issues:
            print(iss.labels)
        
        if issues.totalCount:
            result = True
            issueItem = issues[0]
        
        return result, issueItem

    def _commentOnIssueItem(self, issueItem, comment):
        _commentString = ""
        if instanceof(comment, str):
            _commentString = comment
        elif instanceof(comment, object):
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


    pass

if __name__ == "__main__":

    GITHUB_API_KEY = sys.argv[1]
    commentString = sys.argv[2]
    date = "2022-10-11"
    saver = dataSaver(GITHUB_API_KEY, date)

    res, issueItem = saver._getIssueItemByDate(123)
    if res:
        saver._commentOnIssueItem(issueItem, commentString)



    # saver._getAllcommentsInIssue(1)