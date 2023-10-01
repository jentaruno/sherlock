from notify import QueryNotify
from result import QueryStatus, QueryResult
from sherlock import jsonify_sites
import queue

class QueryNotifyQueue(QueryNotify):
    """Query Notify Queue Object.

    Query notify class that adds results to a queue.
    """

    def __init__(self, result=None, verbose=False, print_all=False, browse=False):
        """Create Query Notify Print Object.

        Contains information about a specific method of notifying the results
        of a query.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.
        verbose                -- Boolean indicating whether to give verbose output.
        print_all              -- Boolean indicating whether to only print all sites, including not found.
        browse                 -- Boolean indicating whether to open found sites in a web browser.

        Return Value:
        Nothing.
        """

        super().__init__(result)
        self.verbose = verbose
        self.print_all = print_all
        self.browse = browse
        self.queue = queue.SimpleQueue()

        return 

    def queueEmpty(self):
        """
        Returns whether the queue holding messages is empty.

        Return value:
        boolean
        """
        return self.queue.empty()

    def queuePop(self):
        """
        Removes and returns the next item from the message queue.
        If the queue is empty, returns None.

        Return value:
        JSON object
        """

        if self.queue.empty():
            return None
        return self.queue.get(True)

    def start(self, message):
        """Notify Start.
        
        Adds the search start message to the queue as JSON.

        Keyword Arguments:
        self                   -- This object.
        message                -- String containing username that the series
                                  of queries are about.

        Return Value:
        Nothing.
        """

        self.queue.put({
            "start": message
        })

    def update(self, result):
        """Notify Update.

        Adds the update to the queue as a JSON object.

        Keyword Arguments:
        self                   -- This object.
        result                 -- Object of type QueryResult() containing
                                  results for this query.

        Return Value:
        Nothing.
        """

        if result.status == QueryStatus.CLAIMED:
            rsp = {
                "site": result.site_name,
                "urlMain": result.site_url_user,
                "urlUser": result.site_url_user,
                "status": str(result.status),
                "httpStatus": result.http_status,
                "responseTime": result.query_time
            }
            self.queue.put({
                "site": rsp
            })

    def finish(self, message="Search completed"):
        """Notify Finish.
        Adds the search finish message to the queue as JSON.
        Keyword Arguments:
        self                   -- This object.
        message                -- The 2 last phrases.
        Return Value:
        Nothing.
        """

        print("stop")
        self.queue.put({
            "stop": message
        }) 