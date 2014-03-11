using System.Runtime.Serialization;

namespace SpotterDataTransferObject.PythonComm
{
    /// <summary>
    /// Class for handling python's json replies - Ping
    /// </summary>
    [DataContract]
    public class PingReply
    {
        /// <summary>
        /// Gets or sets the ip.
        /// </summary>
        /// <value>
        /// The ip.
        /// </value>
        [DataMember(Name = "ip")]
        public string Ip { get; set; }

        /// <summary>
        /// Gets or sets the average.
        /// </summary>
        /// <value>
        /// The average.
        /// </value>
        [DataMember(Name = "avg")]
        public string Avg { get; set; }
    }
}