# Withheld and uncaptured material

This folder publishes the signed core of the run: events, artifacts, constraint records and public identity documents. This file lists everything else that was in the captured copy of the two vaults, and what was never captured. SHA-256 values were computed on the captured copy with `sha256sum`. Paths are relative to the root of that copy (`<vault>/vault/...`). If any listed file is revealed later, `sha256sum -c` against these lines shows whether it is the same file.

## 1. Superseded work: each vault's `.tombstoned/` folder (withheld)

The items in `.tombstoned/` were moved there at 12:51:49–12:51:50 UTC and 13:41:32 UTC on 2026-05-04. Both times are before Loop 2 began (the first published event is at 13:42:09 UTC). The folder holds:
- superseded work: demo and handshake tests, "dream cycle" tests, a smoke test and Loop 1;
- earlier copies of each vault's README and manifest;
- for every item, an unsigned `.tombstone-meta.json` sidecar recording the original path and the time it was moved.

In total it contains 69 signed events in 20 chain files (timestamps 12:16:15 to 13:40:50 UTC) and 25 artifacts. They were checked before being withheld and all verify under the rules in VERIFY.md (69/69 events, 25/25 artifacts). They are withheld because they come before the run the README describes and do not bear on its claims. Artifact names hold a `:`. On Windows copies that character is stored as U+F03A.

108 files:

```
88111b4fd339db01d455f511adbe15757ac1a30428108a4096caf0197d3f9139  cto01/vault/.tombstoned/README.md-2026-05-04T12-51-50.163769Z
01e4ded8b89c017863e0ec35ac94f83fe42f8636b32332d8d57aae5ebf873a2d  cto01/vault/.tombstoned/README.md-2026-05-04T12-51-50.163769Z.tombstone-meta.json
88111b4fd339db01d455f511adbe15757ac1a30428108a4096caf0197d3f9139  cto01/vault/.tombstoned/README.md-2026-05-04T13-41-32.930609Z
47e742f827ae6591e6ffbdf5f32975fa5032489021913c6d4920a498f6f393e3  cto01/vault/.tombstoned/README.md-2026-05-04T13-41-32.930609Z.tombstone-meta.json
7e5948f13941637e462a996fc6def21d64e2d19c7f7986d9e9bef727d708519a  cto01/vault/.tombstoned/artifacts/blake2b-256:12f1ca7abdc6a99db3fccdc1286b884e23c5ad2bba3127447f0ce811d005aaa8.json-2026-05-04T12-51-50.161205Z
c672dcc476851b76bd64273fc4002813f77a4f4b32441b4495fce2970e9b2996  cto01/vault/.tombstoned/artifacts/blake2b-256:12f1ca7abdc6a99db3fccdc1286b884e23c5ad2bba3127447f0ce811d005aaa8.json-2026-05-04T12-51-50.161205Z.tombstone-meta.json
2f3a0e1dbe0ff39129b054cbd3cd14a029d79f8c00370f74ec83235d227bb163  cto01/vault/.tombstoned/artifacts/blake2b-256:241b6a4ba8840510520c7184cb1da04a4310754d58d271438ff5eeb2662da2be.json-2026-05-04T13-41-32.925871Z
98d41908b809a5c7187a3e38eaaf4ee8d5ae0fa0e5d24e7ab91f60377054050b  cto01/vault/.tombstoned/artifacts/blake2b-256:241b6a4ba8840510520c7184cb1da04a4310754d58d271438ff5eeb2662da2be.json-2026-05-04T13-41-32.925871Z.tombstone-meta.json
29ec6ed4a71e7afe242be36b02afc88b8843597b44c3e50899f81bc8025e8b9c  cto01/vault/.tombstoned/artifacts/blake2b-256:291c28495a042349fe1dc57405751871fe17a2e0d57ad017688ca3de84bf5f58.json-2026-05-04T13-41-32.924952Z
295f08fa8dfcfd12d52d8c17066591f349216dc8aa32b5d07199449ce3ee4c46  cto01/vault/.tombstoned/artifacts/blake2b-256:291c28495a042349fe1dc57405751871fe17a2e0d57ad017688ca3de84bf5f58.json-2026-05-04T13-41-32.924952Z.tombstone-meta.json
bb55a075cde799532552360ce14f85075d8f0ff2ce450469f9aac2e4da05dd96  cto01/vault/.tombstoned/artifacts/blake2b-256:4639615534cdcc79ff54b8bc6e2010d503c8e5aab578e4c249cff51b07c77669.json-2026-05-04T12-51-50.159991Z
2b69feaecc4b5464d038c3dd832ae79e4558b96a14e02bb97708e88b92450f7d  cto01/vault/.tombstoned/artifacts/blake2b-256:4639615534cdcc79ff54b8bc6e2010d503c8e5aab578e4c249cff51b07c77669.json-2026-05-04T12-51-50.159991Z.tombstone-meta.json
7d7522b2dbbc20224a73eae31206a6e922a7eff86231a1aff49065836b609c87  cto01/vault/.tombstoned/artifacts/blake2b-256:60ba65f9df1baea739454965c4363fb5efed4aa4f46b23f3228803c383bdd3b9.json-2026-05-04T13-41-32.928903Z
b64db3af29ec576f0b5682f001b8cf4d6f888adb0fa5be09d514e7b98f94b508  cto01/vault/.tombstoned/artifacts/blake2b-256:60ba65f9df1baea739454965c4363fb5efed4aa4f46b23f3228803c383bdd3b9.json-2026-05-04T13-41-32.928903Z.tombstone-meta.json
c1743364bc636d6fa77f001b67b568bde1f6f34ff2474b4b7f2598f09931d9d0  cto01/vault/.tombstoned/artifacts/blake2b-256:6c1985edbe767c3328ea3029c100c4f8856b5bab9e2836cb2d2b77611858036b.json-2026-05-04T13-41-32.925471Z
1252bd5e6e980f516410ee20ab6fc2321bd36ae269b4fbbb12eae0fdc3091948  cto01/vault/.tombstoned/artifacts/blake2b-256:6c1985edbe767c3328ea3029c100c4f8856b5bab9e2836cb2d2b77611858036b.json-2026-05-04T13-41-32.925471Z.tombstone-meta.json
fa313893dabac04198f820833494335b4759e3d41871ffaa65190184179a5010  cto01/vault/.tombstoned/artifacts/blake2b-256:70f48392d891a430ef888192c93e89fcc760ca1da5b195e8b1e0d0080dbcd7f0.json-2026-05-04T13-41-32.927387Z
1e5724bea3506447624e4922fbab961be7bdf427bd46c30b8c9933fd57c3c977  cto01/vault/.tombstoned/artifacts/blake2b-256:70f48392d891a430ef888192c93e89fcc760ca1da5b195e8b1e0d0080dbcd7f0.json-2026-05-04T13-41-32.927387Z.tombstone-meta.json
0f717a908ebb9845dd0f04ecc7e23e0b6e05bed0fa6536d45d73bcd1499618be  cto01/vault/.tombstoned/artifacts/blake2b-256:7bbbd90057bb27ded72b006e7b49af7f2c6f67d8f46ebd3abf9b940ef18716fe.json-2026-05-04T13-41-32.926615Z
84a598cfe6c43f040b21560f7b9c5278b08b9c2031a9806cf42c7d954b621681  cto01/vault/.tombstoned/artifacts/blake2b-256:7bbbd90057bb27ded72b006e7b49af7f2c6f67d8f46ebd3abf9b940ef18716fe.json-2026-05-04T13-41-32.926615Z.tombstone-meta.json
bf6993f96d00e11fa8b37b922abeacd90e6e7ce637c5b6d2719e430c685a28dc  cto01/vault/.tombstoned/artifacts/blake2b-256:871941ec76805dc407aea2a63ef99f7d95357783130ee6632a0ae3d56ad8be62.json-2026-05-04T13-41-32.928170Z
fad5fd6a1da81b552aefe2762a485445061687b7b97d0a1b657089e191493fcf  cto01/vault/.tombstoned/artifacts/blake2b-256:871941ec76805dc407aea2a63ef99f7d95357783130ee6632a0ae3d56ad8be62.json-2026-05-04T13-41-32.928170Z.tombstone-meta.json
75ee936798b3736efaea7b159bd33d90649564cf5dc9cb0829aaf646962c4b56  cto01/vault/.tombstoned/artifacts/blake2b-256:8a81fc590e5fde53d55685be9aa380352460867829032f9db5eb972cd8e92f18.json-2026-05-04T13-41-32.927726Z
25a8977f9752f56f7e9686951eb81f7f507bb32d7408a2d8779d48d9b9407f32  cto01/vault/.tombstoned/artifacts/blake2b-256:8a81fc590e5fde53d55685be9aa380352460867829032f9db5eb972cd8e92f18.json-2026-05-04T13-41-32.927726Z.tombstone-meta.json
bfc53e509b2a7e1b534f8f7afe20f55d284134b775cea7964055be9a0fd8193e  cto01/vault/.tombstoned/artifacts/blake2b-256:8c8b3e670247c09573c3f9cbfb52bad357631ffa7b52a5a0dfaad2b60834a2a8.json-2026-05-04T12-51-50.160598Z
8e890e29e78ab097b001a63979c8714872f02c6d9e3b1ed6e0c2d82498a05533  cto01/vault/.tombstoned/artifacts/blake2b-256:8c8b3e670247c09573c3f9cbfb52bad357631ffa7b52a5a0dfaad2b60834a2a8.json-2026-05-04T12-51-50.160598Z.tombstone-meta.json
f0085556236d80c80b23e5fc9488199c6ef12963e1b1a4eb6f9b0a2641631b09  cto01/vault/.tombstoned/artifacts/blake2b-256:a4924a8fc28bc474859161f6f8317c071baa3ea132fce4fdd1de4b298d895dda.json-2026-05-04T13-41-32.928556Z
70f10c923ba35bded10570c5e91dc94250eb16e90253df6fe20071e5098a6528  cto01/vault/.tombstoned/artifacts/blake2b-256:a4924a8fc28bc474859161f6f8317c071baa3ea132fce4fdd1de4b298d895dda.json-2026-05-04T13-41-32.928556Z.tombstone-meta.json
f701b1ec576997ecdc4e2b378acf79d15a96001b949bea477cb00806cb899d9a  cto01/vault/.tombstoned/artifacts/blake2b-256:c01ed886ea17423dc66363fe369c72c262400b0cc7ce3a9ab446bea69c50b273.json-2026-05-04T13-41-32.927029Z
1db64552dfac2ebaf423083825a1327d3b2dc309ca5ed01f944f756cd874627c  cto01/vault/.tombstoned/artifacts/blake2b-256:c01ed886ea17423dc66363fe369c72c262400b0cc7ce3a9ab446bea69c50b273.json-2026-05-04T13-41-32.927029Z.tombstone-meta.json
2a1bfce88412652f33ed13b57d45ee7ca27ffe60bed3317f8d2c4ec663be1069  cto01/vault/.tombstoned/artifacts/blake2b-256:cbdb17e8c3ae2e710b93b91221b4a47b83ad85d5256bb9bf07c294f2043c11d3.json-2026-05-04T12-51-50.157975Z
1394c0501cb95f591f7059a76c0edadea842cf952733264abcc7f84b39526d32  cto01/vault/.tombstoned/artifacts/blake2b-256:cbdb17e8c3ae2e710b93b91221b4a47b83ad85d5256bb9bf07c294f2043c11d3.json-2026-05-04T12-51-50.157975Z.tombstone-meta.json
fb6a2a1155778a840c90205c39c70a99a72df4b220dcf3eb7455835a41f13176  cto01/vault/.tombstoned/artifacts/blake2b-256:e535caef88aaa5df6bf1f5834cefbffe64e3633f91267c912074e43113f797e5.json-2026-05-04T12-51-50.158784Z
7deb2a6e14edae72e6f56d9a4d287c21be1c571c605c284f055f4cfadb152a48  cto01/vault/.tombstoned/artifacts/blake2b-256:e535caef88aaa5df6bf1f5834cefbffe64e3633f91267c912074e43113f797e5.json-2026-05-04T12-51-50.158784Z.tombstone-meta.json
269cf018522dd2ab24d98b531d241d9f47d0cc70968fc2eccfc138f97bf59739  cto01/vault/.tombstoned/artifacts/blake2b-256:fafa299175b03c80b98013cdd98eda99624740eeda4381bda2910d5340c9345e.json-2026-05-04T13-41-32.926262Z
92f44754a4d4af319b4450a97e5d7afdfffe3b7e96bb5293696c9e55ff51bfac  cto01/vault/.tombstoned/artifacts/blake2b-256:fafa299175b03c80b98013cdd98eda99624740eeda4381bda2910d5340c9345e.json-2026-05-04T13-41-32.926262Z.tombstone-meta.json
f80e4cf619fb372287acb99bea79438d61064dfa1696801bd74dbdeff650685b  cto01/vault/.tombstoned/event_log/artifact-demo-001.jsonl-2026-05-04T12-51-50.155677Z
7becb24c17a961d3852f9abcbd96e3d861edc7c2909c19e2c984ab55cfa030ac  cto01/vault/.tombstoned/event_log/artifact-demo-001.jsonl-2026-05-04T12-51-50.155677Z.tombstone-meta.json
edb647db386c4f1c92317d41bf7412f3be8a5915072de65b4aa59a4d758c7fad  cto01/vault/.tombstoned/event_log/demo-handshake-001.jsonl-2026-05-04T12-51-50.156465Z
52faab478b7ed8902eecef99f910cd72b2197f2f4187c55702bc116409a9ef1c  cto01/vault/.tombstoned/event_log/demo-handshake-001.jsonl-2026-05-04T12-51-50.156465Z.tombstone-meta.json
4d0ff4c49117616af422264b91219d7a6a202be925b29348bfeed46aba6bcfe2  cto01/vault/.tombstoned/event_log/dream-cycle-01.jsonl-2026-05-04T12-51-50.154557Z
5b007db99cc9779924f97cb54169a7ddcf1d67b5abcaf6c476a29c90961f0dda  cto01/vault/.tombstoned/event_log/dream-cycle-01.jsonl-2026-05-04T12-51-50.154557Z.tombstone-meta.json
098b50b01d77b0f5c408832d73cb12abf9c27e39dea33f2f8959afe4e8bc49a1  cto01/vault/.tombstoned/event_log/dream-cycle-02.jsonl-2026-05-04T13-41-32.922760Z
2999d11d03dfda4e8b0e89d0b8bdabd6eb538d6ef281d288bdf9bbd6f7003f31  cto01/vault/.tombstoned/event_log/dream-cycle-02.jsonl-2026-05-04T13-41-32.922760Z.tombstone-meta.json
85329c6c20d6a2b2799fd9d1712f6d18e60d8d1405bb846d1081273526f8d607  cto01/vault/.tombstoned/event_log/dream-cycle-03-heterogeneous.jsonl-2026-05-04T13-41-32.921384Z
40f60091b738361e3d7ac339e0aa36192dd6d5b3417a6c7d74b470fe55c8f93e  cto01/vault/.tombstoned/event_log/dream-cycle-03-heterogeneous.jsonl-2026-05-04T13-41-32.921384Z.tombstone-meta.json
cd102d47b114db967004c57f33027aff900561d7627c3708a126e6ebf5793d5f  cto01/vault/.tombstoned/event_log/loop1-step1-design.jsonl-2026-05-04T13-41-32.922042Z
4f2d5e95aa1fb194435201af63e5ae53a8eac6c4a37c4b2c56b06faa1ce9ae65  cto01/vault/.tombstoned/event_log/loop1-step1-design.jsonl-2026-05-04T13-41-32.922042Z.tombstone-meta.json
41bfe509d10ff87fa963baf64c07df4ed153c9f0117af8f82c86756771115578  cto01/vault/.tombstoned/event_log/loop1-step2-implement.jsonl-2026-05-04T13-41-32.922403Z
28dae9a451145b88db93a1c7e1d96b6ffa7cbdbf07b0c917422f3807a05735da  cto01/vault/.tombstoned/event_log/loop1-step2-implement.jsonl-2026-05-04T13-41-32.922403Z.tombstone-meta.json
d930187ceed0b1caf6cd197af977b93df97eec7ca4ca92943661acfbb8fc1a24  cto01/vault/.tombstoned/event_log/loop1-step4-simulate.jsonl-2026-05-04T13-41-32.923557Z
77c6ab6341e7c7de593420cc22b7b8e83c3d7482d9b67d5d0a7c1c9545678eb1  cto01/vault/.tombstoned/event_log/loop1-step4-simulate.jsonl-2026-05-04T13-41-32.923557Z.tombstone-meta.json
3af13f0360deda7dd9da84e79d7b0db56017204620403b7de9d69d418e1cef20  cto01/vault/.tombstoned/event_log/loop1-step5-refine.jsonl-2026-05-04T13-41-32.923102Z
171afb79862dc04ab3ae3434fcfc756c66c5cf803f599ff11975556ce9b37d12  cto01/vault/.tombstoned/event_log/loop1-step5-refine.jsonl-2026-05-04T13-41-32.923102Z.tombstone-meta.json
e460b725401698dcc43a5bbe448968e75ef0da184e918400874ae3335ebcf2fc  cto01/vault/.tombstoned/event_log/smoke-id-test.jsonl-2026-05-04T13-41-32.923947Z
17f2d0d1a52b6d6f31b8d7c711d9041bf2907f96c11d5a1eb5b78b5897a348c1  cto01/vault/.tombstoned/event_log/smoke-id-test.jsonl-2026-05-04T13-41-32.923947Z.tombstone-meta.json
15e17ae23a265181e769f0038fae92ea57dd163112757e9bc6c4d472820516ee  cto01/vault/.tombstoned/manifest.json-2026-05-04T12-51-50.167055Z
aadcf0d8a2548c5c85ba2751259d14f62a9a76d833be55c1a1e002f716611a20  cto01/vault/.tombstoned/manifest.json-2026-05-04T12-51-50.167055Z.tombstone-meta.json
e64528203bd0244b29ee0c40406ee635ed37963192d9af8a1563c5770e6d9b42  cto01/vault/.tombstoned/manifest.json-2026-05-04T13-41-32.932698Z
2e261f4bb4839b02a92520b46f5d3746c775c90a152bd3b5dd4773dfb1428cb9  cto01/vault/.tombstoned/manifest.json-2026-05-04T13-41-32.932698Z.tombstone-meta.json
88111b4fd339db01d455f511adbe15757ac1a30428108a4096caf0197d3f9139  test01/vault/.tombstoned/README.md-2026-05-04T12-51-49.983763Z
16d61311b681425f0fd2c4696632b192a9047caedc4c2f163205cac3a752f18e  test01/vault/.tombstoned/README.md-2026-05-04T12-51-49.983763Z.tombstone-meta.json
88111b4fd339db01d455f511adbe15757ac1a30428108a4096caf0197d3f9139  test01/vault/.tombstoned/README.md-2026-05-04T13-41-32.741984Z
bf4c6978043f9c52b3afaa954a34b8a97d098bf49464ec86cd05a5f62e24423f  test01/vault/.tombstoned/README.md-2026-05-04T13-41-32.741984Z.tombstone-meta.json
7e5948f13941637e462a996fc6def21d64e2d19c7f7986d9e9bef727d708519a  test01/vault/.tombstoned/artifacts/blake2b-256:12f1ca7abdc6a99db3fccdc1286b884e23c5ad2bba3127447f0ce811d005aaa8.json-2026-05-04T12-51-49.988053Z
f00aa4df5701dd235c52db3218819764f54ee0ee9c14675bd58c61646ff51f91  test01/vault/.tombstoned/artifacts/blake2b-256:12f1ca7abdc6a99db3fccdc1286b884e23c5ad2bba3127447f0ce811d005aaa8.json-2026-05-04T12-51-49.988053Z.tombstone-meta.json
6edc40c5016e15672460958672c04a8b8a9423297691eceaad426f86a557afa6  test01/vault/.tombstoned/artifacts/blake2b-256:30c3c445886bd2b11ec1e759232de5dee20d9c97401e01bef91ffce3b943f269.json-2026-05-04T13-41-32.748089Z
bd3794bdac4512cbbc1a5fc3dfd3a480609cfc83edb06d9c18f534ecee3aff8d  test01/vault/.tombstoned/artifacts/blake2b-256:30c3c445886bd2b11ec1e759232de5dee20d9c97401e01bef91ffce3b943f269.json-2026-05-04T13-41-32.748089Z.tombstone-meta.json
bb55a075cde799532552360ce14f85075d8f0ff2ce450469f9aac2e4da05dd96  test01/vault/.tombstoned/artifacts/blake2b-256:4639615534cdcc79ff54b8bc6e2010d503c8e5aab578e4c249cff51b07c77669.json-2026-05-04T12-51-49.988590Z
64154189a7d8c1836be497eed65bcc644e4b829b39cd6b7b5954320288628902  test01/vault/.tombstoned/artifacts/blake2b-256:4639615534cdcc79ff54b8bc6e2010d503c8e5aab578e4c249cff51b07c77669.json-2026-05-04T12-51-49.988590Z.tombstone-meta.json
3c9339b9ce0f7095144fac4eb575d9f0484052f32e48501dfb254c0a1fba0bdf  test01/vault/.tombstoned/artifacts/blake2b-256:5f9e4aa4143b7ca7c28304c53c2e362b3562326a906dd2ac75b1e3a129587fbb.json-2026-05-04T13-41-32.749017Z
c78b531594ab2782c3a7ea7447cd228652c956951f50c8a480f73c0c6ff5d696  test01/vault/.tombstoned/artifacts/blake2b-256:5f9e4aa4143b7ca7c28304c53c2e362b3562326a906dd2ac75b1e3a129587fbb.json-2026-05-04T13-41-32.749017Z.tombstone-meta.json
7d7522b2dbbc20224a73eae31206a6e922a7eff86231a1aff49065836b609c87  test01/vault/.tombstoned/artifacts/blake2b-256:60ba65f9df1baea739454965c4363fb5efed4aa4f46b23f3228803c383bdd3b9.json-2026-05-04T13-41-32.748618Z
00a9e7479a133fb90301c6801cf02921757e5a6ddc90be8e8f673b068ba0fa59  test01/vault/.tombstoned/artifacts/blake2b-256:60ba65f9df1baea739454965c4363fb5efed4aa4f46b23f3228803c383bdd3b9.json-2026-05-04T13-41-32.748618Z.tombstone-meta.json
c1743364bc636d6fa77f001b67b568bde1f6f34ff2474b4b7f2598f09931d9d0  test01/vault/.tombstoned/artifacts/blake2b-256:6c1985edbe767c3328ea3029c100c4f8856b5bab9e2836cb2d2b77611858036b.json-2026-05-04T13-41-32.749404Z
3744a2e342e2a9dfde869bca99e314fe9d6adeda7df23f5a9e0b3612e16b055a  test01/vault/.tombstoned/artifacts/blake2b-256:6c1985edbe767c3328ea3029c100c4f8856b5bab9e2836cb2d2b77611858036b.json-2026-05-04T13-41-32.749404Z.tombstone-meta.json
bfc53e509b2a7e1b534f8f7afe20f55d284134b775cea7964055be9a0fd8193e  test01/vault/.tombstoned/artifacts/blake2b-256:8c8b3e670247c09573c3f9cbfb52bad357631ffa7b52a5a0dfaad2b60834a2a8.json-2026-05-04T12-51-49.988908Z
64b4f0603d8ad0565b2a1aad2e1de00d9af90a0dd7b6ad8d33eff089fdfb154b  test01/vault/.tombstoned/artifacts/blake2b-256:8c8b3e670247c09573c3f9cbfb52bad357631ffa7b52a5a0dfaad2b60834a2a8.json-2026-05-04T12-51-49.988908Z.tombstone-meta.json
f701b1ec576997ecdc4e2b378acf79d15a96001b949bea477cb00806cb899d9a  test01/vault/.tombstoned/artifacts/blake2b-256:c01ed886ea17423dc66363fe369c72c262400b0cc7ce3a9ab446bea69c50b273.json-2026-05-04T13-41-32.749753Z
be4f14c1f54acd03af26c22e2197ab6c868270299b31729729cb80889b4b0902  test01/vault/.tombstoned/artifacts/blake2b-256:c01ed886ea17423dc66363fe369c72c262400b0cc7ce3a9ab446bea69c50b273.json-2026-05-04T13-41-32.749753Z.tombstone-meta.json
2a1bfce88412652f33ed13b57d45ee7ca27ffe60bed3317f8d2c4ec663be1069  test01/vault/.tombstoned/artifacts/blake2b-256:cbdb17e8c3ae2e710b93b91221b4a47b83ad85d5256bb9bf07c294f2043c11d3.json-2026-05-04T12-51-49.989304Z
6d175ae08d5a2298b2c8ee83076f09ca6d1dcda3b879ab3d9b1cffe1e0318309  test01/vault/.tombstoned/artifacts/blake2b-256:cbdb17e8c3ae2e710b93b91221b4a47b83ad85d5256bb9bf07c294f2043c11d3.json-2026-05-04T12-51-49.989304Z.tombstone-meta.json
18188f71c1f0110c1d9c5d9e364daf05256ba74bce675f86a2ddaeae09c79e36  test01/vault/.tombstoned/event_log/artifact-demo-001.jsonl-2026-05-04T12-51-49.986726Z
637a027a2dd2326c04e6adc4fc3f4257d64da0dfb846a474b6ebff6ca9cfd03b  test01/vault/.tombstoned/event_log/artifact-demo-001.jsonl-2026-05-04T12-51-49.986726Z.tombstone-meta.json
c62a6c26a8367200826cb16c274c14ac0762ce0034aa06313761bef75b7d3d4a  test01/vault/.tombstoned/event_log/demo-handshake-001.jsonl-2026-05-04T12-51-49.987668Z
8383b9df0c1b1b974f4bb966f230de6c4f8777ad06ebab8366ad15efed43b7fc  test01/vault/.tombstoned/event_log/demo-handshake-001.jsonl-2026-05-04T12-51-49.987668Z.tombstone-meta.json
fffb9035733ba06938a7e89d354ea36503f4e100586c8abf6e9370cf1b2b4903  test01/vault/.tombstoned/event_log/dream-cycle-01.jsonl-2026-05-04T12-51-49.987107Z
8f582963dc6f67560e474f90550950c59d58e34dd2218633f5b917a1d3171745  test01/vault/.tombstoned/event_log/dream-cycle-01.jsonl-2026-05-04T12-51-49.987107Z.tombstone-meta.json
5b1ace1fd93933b6a85692cb17c3ad8f5bb30475ef419851606f328a06142974  test01/vault/.tombstoned/event_log/dream-cycle-02.jsonl-2026-05-04T13-41-32.746023Z
a6000a20e7dbca9431ff5c59d9c77d47adb503ed477f1232f72e9c034c82411f  test01/vault/.tombstoned/event_log/dream-cycle-02.jsonl-2026-05-04T13-41-32.746023Z.tombstone-meta.json
10ef37a1ec2bc0eda74c4432f28a163e53326d08c138b9b29ce4fa3e21cb84fb  test01/vault/.tombstoned/event_log/dream-cycle-03-heterogeneous.jsonl-2026-05-04T13-41-32.744939Z
02f1c7657f052be74608e8623462eda56b046a8ddee98d4acb301ed3a0e1d989  test01/vault/.tombstoned/event_log/dream-cycle-03-heterogeneous.jsonl-2026-05-04T13-41-32.744939Z.tombstone-meta.json
59d2a140f0a399a8739d2b3932ad38b99aa238d9c49bfa7749180d134c9b580d  test01/vault/.tombstoned/event_log/loop1-step1-design.jsonl-2026-05-04T13-41-32.746712Z
05eebef4c812216048ada6f93a91a251852fa66c1a1ba3c6391b9db3896396c1  test01/vault/.tombstoned/event_log/loop1-step1-design.jsonl-2026-05-04T13-41-32.746712Z.tombstone-meta.json
1042cf21ae4eca1fef2cfd6fdfa38724968a76789672ea814ecc4022750e3636  test01/vault/.tombstoned/event_log/loop1-step2-implement.jsonl-2026-05-04T13-41-32.746380Z
02609c9d5b8d052e166973f89dee7b67a0cc0fb0785069c27722109974984f85  test01/vault/.tombstoned/event_log/loop1-step2-implement.jsonl-2026-05-04T13-41-32.746380Z.tombstone-meta.json
33c0a6488e1597b18ddbdf39ba2d0712bc0ae6c9b50ed6c4cfd7ec5dc31456f3  test01/vault/.tombstoned/event_log/loop1-step4-simulate.jsonl-2026-05-04T13-41-32.747031Z
38aedc649af2c057a7b2a6a23dae406eea171c128e031937aef71534321e73fa  test01/vault/.tombstoned/event_log/loop1-step4-simulate.jsonl-2026-05-04T13-41-32.747031Z.tombstone-meta.json
2251072b73549ce3deb0c291a9f0bb0a9553a53f1b4a269ad5b936424fc161ec  test01/vault/.tombstoned/event_log/loop1-step5-refine.jsonl-2026-05-04T13-41-32.747487Z
d115129c71e7e5acba4dbfd71bf253a19fe64d26d822c7174701e4e4b9592aca  test01/vault/.tombstoned/event_log/loop1-step5-refine.jsonl-2026-05-04T13-41-32.747487Z.tombstone-meta.json
a0a848822d145894d9ffec51414648db744f295b570aabe1022ea2660b03d659  test01/vault/.tombstoned/event_log/smoke-id-test.jsonl-2026-05-04T13-41-32.745621Z
4ad082a42d97699f77e71be5250b9cac63d44f9109176c613a8bd9da1ae3f7c1  test01/vault/.tombstoned/event_log/smoke-id-test.jsonl-2026-05-04T13-41-32.745621Z.tombstone-meta.json
81f3ffa76ded9fcff40635cf041387ab9aa3f6739a008dd403fc967ff6f5a311  test01/vault/.tombstoned/manifest.json-2026-05-04T12-51-49.983127Z
b2060b308957c9b913f0728b71452e7bc7246ee3f487480ac070685bfc7d9089  test01/vault/.tombstoned/manifest.json-2026-05-04T12-51-49.983127Z.tombstone-meta.json
b6ce9a35302e8020e0d01627217b481ff44756ec9b06b9fe570d3b3f2654e9b0  test01/vault/.tombstoned/manifest.json-2026-05-04T13-41-32.741136Z
711e176075c58e1f336ee4041554b5654055b28e7c7a3236b8739ef8abf490ed  test01/vault/.tombstoned/manifest.json-2026-05-04T13-41-32.741136Z.tombstone-meta.json
274eeb36cf503aab1a33c60bf42284d79ce67c6f64351a339c6f7150fa2002b9  test01/vault/.tombstoned/smoke/hello.txt-2026-05-04T12-51-49.986098Z
024946fb115c798a3fe8bc40580a0ba5099d9efe6a5fc486d45666ad946877fe  test01/vault/.tombstoned/smoke/hello.txt-2026-05-04T12-51-49.986098Z.tombstone-meta.json
```

## 2. Unsigned wrapper files (not published)

These are the top-level notes of the forensic copy and each vault's `README.md` and `manifest.json`. They are unsigned operator notes and configuration, not part of the signed record. Their contents are summarised, where relevant, in this folder's README.md and VERIFY.md.

```
0a65ec03eea2fc3129f4b287da256064b1b9027a2a15ec5f6c633844fcc3cbae  README.md
88111b4fd339db01d455f511adbe15757ac1a30428108a4096caf0197d3f9139  cto01/vault/README.md
e6a785a6f0ee2dbd945c2589043926078c444f68ae16abe9cc440e46ac9985b2  cto01/vault/manifest.json
88111b4fd339db01d455f511adbe15757ac1a30428108a4096caf0197d3f9139  test01/vault/README.md
99b639e97792a5ad8c361ac290a13ccddd8b4d98d658c5f26cc79baa02851170  test01/vault/manifest.json
```

## 3. Secret material (not published, not hashed here)

The four private-key files (one per identity) and two archives of the vaults that contain them are not published, and no hashes are given for them. See KEYS-RETIRED.md.

## 4. Never captured

- **The third instance.** Its vault and identity document were not captured when the machines were halted. As a result:
  - one artifact the record refers to is absent: `blake2b-256:d54c3c3e1852c3498f16f202280ee83cbf981849b91b9a4a0d94ec6026f3956a`, a review produced on the third instance and listed in `events/test01/loop3-step4-yuki-v3.jsonl`;
  - 2 of test01's 8 recorded delegations (the two review steps) were acknowledged by events that are in neither captured vault;
  - the receipts and validator claims it returned for the 6 artifact transfers cto01 sent to it are not here (6 `witness_event_hash`, 6 `validator_claim_hash`);
  - its signing key appears only as a self-asserted DID inside one artifact (see KEYS-RETIRED.md).
- **Delegation envelopes and earlier constraint versions.** Neither vault stored the delegation envelopes (11 event `subject` values) or the earlier versions of the two constraint records (3 event `subject` values). Each constraint file holds only its state at the halt.
