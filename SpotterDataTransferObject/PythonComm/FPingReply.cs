using System.Runtime.Serialization;

namespace SpotterDataTransferObject.PythonComm
{
    /// <summary>
    /// Class for handling python's json replies - FPing
    /// </summary>
    [DataContract]
    public class FPingReply
    {
        /// <summary>
        /// Gets or sets the ping results.
        /// </summary>
        /// <value>
        /// The ping results.
        /// </value>
        [DataMember(Name = "result")]
        public PingReply[] PingResults { get; set; }
    }
}