# Instruments Where They Belong

A tool does not become useful because it appears in a catalogue. Somewhere, something must be able to perform its work. There must be a machine with the necessary resources, a person entitled to use them, and a means of distinguishing what was requested from what actually happened.

Much of contemporary artificial intelligence obscures this simple arrangement. A person addresses a conversational interface, and the interface appears to contain everything: language, knowledge, computation, documents, music, images, perhaps an entire computer. The machinery disappears behind a single voice. What remains visible is a request and a response.

But the machinery has not disappeared. The question of where work is performed has merely become difficult to ask.

Fountain Coach begins with that question.

An instrument is a bounded capability: something that can be identified, invoked, observed and, where necessary, refused. It might render a manuscript, synthesize sound, inspect a repository, analyze a recording, compose a stage score or publish an edition. Some instruments perform their work entirely in software. Others depend on microphones, cameras, audio interfaces, native applications or particular operating systems. Some complete an operation immediately; others require a durable process that continues after the conversational client has closed.

These differences are not incidental details to be concealed by a common interface. They belong to the identity of the instrument.

A Csound synthesizer requires an audio runtime. A Swift instrument built for Linux requires a compatible Swift environment. An operation that uses an Apple-native media framework belongs on a supported Apple device. A publishing operation may need a server with access to a particular repository and an authorized publication target. No instruction, however intelligently written, can remove these dependencies.

What a common system can do is make the dependencies intelligible.

## A machine of one's own

Consider a customer who operates a small Ubuntu server. It may be a computer at home, a machine at work or a virtual server rented from a provider. Its ownership is practical rather than necessarily physical: the customer controls the operating environment, selects the resources and bears the computing cost.

That machine can become a Fountain Host.

The host runs compatible instruments, maintains durable jobs and exposes precisely declared capabilities to authorized clients. It does not need to be a general-purpose agent improvising commands from natural language. It can provide named operations with specified inputs, permissions, resource boundaries and results.

The customer might address it through ChatGPT, Claude, Reframe or another compatible client. The language model interprets a request and may propose an instrument invocation. It does not thereby acquire ownership of the host, the customer's files or the instrument's execution rules.

The host checks the requested operation against its admitted contract and the customer's authorization. The appropriate instrument performs the work. The result returns with evidence of its execution.

This is a different relationship from buying computation from Fountain Coach.

The customer already has the machine. Fountain Coach supplies the instruments that make it useful for particular purposes, maintains their versions and governs access to them. The customer pays for the right to use the software capabilities, not for the privilege of consuming unlimited computing resources belonging to somebody else.

Such a model does not eliminate infrastructure costs. The customer must still maintain or rent the Ubuntu host. But it removes the need for Fountain Coach to build a speculative fleet of customer execution servers before anyone has purchased an instrument.

## The resources that stay at home

The Ubuntu host cannot do everything. Nor should it.

A manuscript may reside on a Mac. A microphone may be connected to an iPad. A camera may be available on an iPhone. A music application may depend on native audio facilities that do not exist on Linux. The most appropriate place for an operation is often the device where its required resources already live.

A distributed Fountain Coach instrument system therefore needs more than one kind of participant.

The Ubuntu machine provides a persistent execution environment. A Mac may contribute a bounded filesystem operation, a native compilation task or a media-processing capability. An iPad may provide an authored gesture, a document selection, a sound-performance interface or a permitted recording. An iPhone may contribute a selected image or a moment of audio capture.

These are not invitations to take unrestricted control of someone's devices.

The Mac must expose only the resources admitted by its local companion and the user. An iPad or iPhone remains subject to its application's sandbox, operating-system permissions and availability. A mobile device cannot be assumed to act as an always-running remote server merely because it has joined the customer's instrument network. Some operations are possible only while the application is active; others require a supported background mode or a deliberate user interaction.

A remote host should not need to copy an entire photo library to work with one selected photograph. Nor should a publishing instrument require general access to a computer merely to read one approved source document.

The instrument asks for a capability, not possession of the device.

This changes the meaning of connectivity. The relationship between machines is not a permanent opening through which any command may pass. It is an arrangement of narrowly defined permissions, available resources and observable effects.

A device may be absent. A permission may expire. An operation may be refused. These are ordinary conditions of the system, not defects to be overcome by quietly widening access.

## What the customer buys

If the customer supplies the machines and the language model, what remains for Fountain Coach to sell?

The instrument itself—and the continuing work required to make that instrument dependable.

A commercial instrument is more than a downloadable executable. It has an identity, a version, an implementation, supported operating environments and a declared purpose. It has a contract that distinguishes valid requests from invalid ones. It has installation and update procedures. It can report what it did, under which conditions, and whether the result satisfies the operation that was authorized.

It also has a maintained relationship with the system through which the customer discovers and invokes it.

A customer might purchase access to a semantic publishing instrument, for example. The purchase would authorize a particular capability, or a defined family of capabilities, on registered compatible hosts. The customer could then use that instrument through a supported AI client or a dedicated Fountain Coach interface.

The license would not need to include OpenAI or Anthropic inference. Those services remain independently contracted by the customer, subject to their own terms and supported integration methods. A ChatGPT subscription must not be mistaken for unrestricted access to OpenAI's API.

Nor would the instrument license silently include unlimited third-party compute. Most work could run on the customer's own machines. A future managed-execution option, where offered, would require its own price, funding and spending limit.

There is commercial value in this separation. Fountain Coach can charge for maintained capability rather than speculate on the customer's future demand for processing power. The customer's costs remain visible: an instrument entitlement, a machine they control, and any independently chosen AI service.

A purchase opens an authorized use of a capability. It does not purchase the customer's data from them, transfer control of their computers or turn a license into permission for arbitrary remote operations.

The right to run a particular instrument can also end. Revoking an entitlement must prevent subsequent licensed invocations according to the declared contract. It should not strand a customer's machine, destroy their documents or make their own work dependent on the continued availability of an AI vendor.

These distinctions belong in the product, not in an afterthought called terms and conditions.

## One instrument, several possible places

An instrument should not change its meaning simply because it runs somewhere else.

Its name, version, operation contract and expected result can remain stable across execution environments. Its implementation may not.

A Swift package that runs on Ubuntu may be directly installable on another supported Linux host. A related operation on macOS may need an adapter to Apple frameworks. A browser-based audio instrument may execute within an AudioWorklet. An iPad instrument may exist as part of a signed native application. A physical MIDI device may participate through a negotiated hardware connection.

These are multiple implementations or execution paths of a declared capability, not proof that one binary can run everywhere.

Portability must be established by actual testing on each supported platform. A catalogue entry cannot establish it. A successful build on one machine cannot establish it. Nor can a demonstration in a browser substitute for acceptance on a physical iPad.

The instrument's execution description should therefore say where it can run, what it needs, which resources it may access and how the result is verified. A customer purchasing an instrument should be able to distinguish a supported Ubuntu release from an experimental iPad integration.

This is particularly important for Fountain Coach because its instruments do not all belong to the same technological family. Publishing, sound synthesis, stage composition, local media processing, MIDI 2.0 communication and native development operations make different demands on a computer.

They can nevertheless share a governed way of being identified, authorized and invoked.

FCIS-KIT provides the instrument's executable contract. FountainAuthKit provides the basis for authentication and authorization. Fountain Host provides admitted machine capabilities. FountainStore can preserve durable execution evidence where a capability requires it. MCP, MIDI 2.0 and native application interfaces serve different communication and interaction roles; no single transport must be imposed on every operation.

The system is common in its contracts, not homogeneous in its machinery.

## An instrument is not a prompt

There is a tempting shortcut in AI software: give a language model a set of instructions, call those instructions a tool, and assume that the model's compliance establishes the tool's reliability.

Instructions have their place. They can describe a task, guide interpretation and help a model select an appropriate capability. They cannot, on their own, enforce filesystem permissions, establish device consent, guarantee a build result or prove that an external publication occurred.

An instrument has to cross from language into execution.

That crossing should be explicit. A request acquires a typed operation identity. The relevant authority determines whether it is permitted. An implementation executes within its declared boundary. The system distinguishes progress from completion, refusal from failure, and intention from effect.

Where the operation changes something durable, the record should survive the disappearance of the conversational session. A publication does not become successful because a model says that it was published. A software build does not pass because an assistant confidently describes its success.

The machine has to do the work, and the result has to be observed.

This is one reason to keep execution on the customer's own host where practical. The instrument operates against resources the customer controls. The customer need not surrender all of those resources to a remote AI service merely to request a bounded operation.

It is also a reason not to confuse the authority of a language model with the authority of an instrument. The model may help formulate the request. The instrument's contract decides what can actually happen.

## An estate without a compulsory cloud

A distributed system needs a point of coordination. It does not necessarily need a large centralized computing estate.

Fountain Coach could maintain the comparatively small services needed to authenticate customers, manage purchased entitlements, distribute versioned instruments, register authorized hosts and establish permitted client relationships.

The expensive or resource-specific work would remain on the machines suited to it.

A customer with an Ubuntu server might run a persistent publishing or analysis instrument there. The same customer could authorize a Mac to perform a native operation when required. Their iPad could provide an interactive performance surface. An external AI client could request a task without becoming the authority over any of these machines.

Fountain Coach would earn revenue from the capabilities connecting those possibilities, not from owning their processors.

Such an arrangement can also reduce dependence on any particular conversational product. A customer may change AI providers without losing their instrument identities or the machines on which those instruments run. A deterministic operation may need no language model at all. An unavailable client should not make the customer's own host unusable through every other admitted interface.

The economic principle and the technical principle reinforce each other: do not make the customer rent again what they already possess, and do not make Fountain Coach finance a machine that the customer can operate themselves.

There will still be legitimate cases for managed execution. Some customers will not want to administer Ubuntu. Some workloads will require specialized hardware. Some instruments may depend on a controlled publication or processing environment. These can become separately priced services when the necessary infrastructure, usage limits and supplier agreements are established.

They should not become hidden prerequisites for using instruments that can run independently.

## From an owner's estate to a customer's product

Parts of this architecture already exist within Fountain Coach. The owner-operated Fountain Host has demonstrated bounded operations and durable execution mechanisms. Authentication and consent infrastructure has been developed. Instrument contracts, local Swift packages, browser audio engines and publishing systems have different levels of implementation and acceptance.

That is a substantial technical foundation, but it is not yet a commercial product that an unrelated customer can install, purchase and operate without the owner's assistance.

The commercial transition would have to demonstrate something concrete.

A customer purchases one named instrument entitlement. They authenticate with Fountain Coach, enroll a compatible Ubuntu host under their own control and install the admitted instrument release. They invoke it through a supported client. The instrument performs a real operation on that machine and returns its result with verifiable evidence. The customer can inspect what was authorized, suspend or revoke access, and retain control of their computer and data throughout.

A second demonstration would introduce a Mac or iPad resource. That device would contribute a specifically permitted capability and refuse operations outside its grant. It would not be treated as a miniature Ubuntu server, nor would installation imply unrestricted remote access.

Only then would the relationship between purchased access, machine ownership and distributed execution have been established in practice.

An instrument catalogue can explain the offer. A purchase interface can transact it. Neither can replace that demonstration.

## Where the work belongs

The phrase *artificial intelligence* has encouraged us to think of capability as something located inside a model. The model appears to know how to write, draw, listen, compose, compile and publish. Yet each of those verbs can lead to a different material situation: a page being composed, a processor generating sound, a file being read, a microphone becoming active, a program being built, a public edition being delivered.

There is no reason for these situations to occupy the same computer.

There is also no reason for the person who owns the work to lose control of the machines and resources involved simply because the request was expressed in language.

Fountain Coach can treat the instrument as the durable unit of this relationship. The instrument says what can be done. Its execution contract identifies where and under what conditions it can be done. The customer purchases the capability and chooses the resources on which to operate it. The AI, when useful, helps the person address the system.

The work remains where it belongs.

**Your instruments. Your machines. Your authority.**
