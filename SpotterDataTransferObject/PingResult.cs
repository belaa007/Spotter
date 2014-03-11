using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using SpotterDataTransferObject.PythonComm;

namespace SpotterDataTransferObject
{
    /// <summary>
    /// Class for transfering ping results.
    /// </summary>
    [DataContract]
    public class PingResult
    {
        /// <summary>
        /// Gets or sets the nodes.
        /// </summary>
        /// <value>
        /// The nodes.
        /// </value>
        [DataMember]
        public List<Node> Nodes { get; set; }

        /// <summary>
        /// Gets or sets the replies.
        /// </summary>
        /// <value>
        /// The replies.
        /// </value>
        [DataMember]
        public List<PingReply> Replies { get; set; }
    }
}