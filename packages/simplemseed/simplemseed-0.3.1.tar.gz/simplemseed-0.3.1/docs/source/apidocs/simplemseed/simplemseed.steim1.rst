:py:mod:`simplemseed.steim1`
============================

.. py:module:: simplemseed.steim1

.. autodoc2-docstring:: simplemseed.steim1
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`decodeSteim1 <simplemseed.steim1.decodeSteim1>`
     - .. autodoc2-docstring:: simplemseed.steim1.decodeSteim1
          :summary:
   * - :py:obj:`encodeSteim1 <simplemseed.steim1.encodeSteim1>`
     - .. autodoc2-docstring:: simplemseed.steim1.encodeSteim1
          :summary:
   * - :py:obj:`encodeSteim1FrameBlock <simplemseed.steim1.encodeSteim1FrameBlock>`
     - .. autodoc2-docstring:: simplemseed.steim1.encodeSteim1FrameBlock
          :summary:
   * - :py:obj:`extractSteim1Samples <simplemseed.steim1.extractSteim1Samples>`
     - .. autodoc2-docstring:: simplemseed.steim1.extractSteim1Samples
          :summary:

API
~~~

.. py:function:: decodeSteim1(dataBytes: bytearray, numSamples, bias)
   :canonical: simplemseed.steim1.decodeSteim1

   .. autodoc2-docstring:: simplemseed.steim1.decodeSteim1

.. py:function:: encodeSteim1(samples: list[int], frames: int = 0, bias: int = 0, offset: int = 0) -> bytearray
   :canonical: simplemseed.steim1.encodeSteim1

   .. autodoc2-docstring:: simplemseed.steim1.encodeSteim1

.. py:function:: encodeSteim1FrameBlock(samples: list[int], frames: int = 0, bias: int = 0, offset: int = 0) -> simplemseed.steimframeblock.SteimFrameBlock
   :canonical: simplemseed.steim1.encodeSteim1FrameBlock

   .. autodoc2-docstring:: simplemseed.steim1.encodeSteim1FrameBlock

.. py:function:: extractSteim1Samples(dataBytes: bytearray, offset: int) -> list
   :canonical: simplemseed.steim1.extractSteim1Samples

   .. autodoc2-docstring:: simplemseed.steim1.extractSteim1Samples
