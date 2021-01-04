from aiohttp import web
import handler_edit


class XMLRPCExample(handler_edit.XMLRPCView):
    def rpc_test(self):
        return None

    def rpc_args(self, *args):
        return len(args)

    def rpc_kwargs(self, **kwargs):
        return len(kwargs)

    def rpc_args_kwargs(self, *args, **kwargs):
        return len(args) + len(kwargs)

    def rpc_exception(self):
        raise Exception("YEEEEEE!!!")


app = web.Application()
app.router.add_route('*', '/', XMLRPCExample)

if __name__ == "__main__":
    web.run_app(app)
