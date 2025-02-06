# Demo Faas platform using resonate

## Why Build an On-Premise FaaS Platform?

Function-as-a-Service (FaaS) is a cloud computing model that lets developers
deploy individual pieces of code—called functions—without managing servers or
infrastructure. These functions are triggered by specific events, like an HTTP
request, a file upload, or a database update. The cloud provider
(e.g., AWS Lambda, Azure Functions) automatically handles scaling, resource
allocation, and runtime environments. You pay only for the compute time your
functions consume, in millisecond increments.

The "serverless" nature of FaaS means developers focus purely on writing code
to solve problems, while the provider abstracts away servers, virtual machines,
and containers. However, "serverless" doesn’t mean there are no servers—it
means you don’t see or manage them.

The idea of building an on-premise Function-as-a-Service
(FaaS) platform might seem counterintuitive. Isn’t the whole point of FaaS to
be “serverless,” abstracting away the infrastructure so you don’t have to worry
about servers? The answer lies in the unique benefits that an on-premise FaaS
platform can offer, especially for specific use cases like GPU and AI workloads
or sensitive data processing.

## Why Resonate?

Resonate is designed to make distributed systems as straightforward as writing
`async/await` code. This property makes it great to write an on-prem FaaS
platform as it abstracts away the complexities of distributed systems,
providing:

- Distributed Async/Await: Write functions as simple `async/await` code while
  Resonate guarantees crash-resistant execution.
- Routing: Tasks are directed to the right workers seamlessly, thanks to
  Resonate’s task framework and distributed event loop. This allows the FaaS
  platform to direct the workload based on user input or other defined criteria.
- Durability: Automatic retries and built-in replayability ensure functions
  survive hardware failures and network issues.

These features make Resonate an excellent choice for building our demo FaaS
platform, especially for on-premise use cases where control, security,
and cost predictability are critical.
