// transcode <src> <dst.mp4> <width> <bitrate-bps>: H.264, no audio, faststart
import AVFoundation
let a = CommandLine.arguments
let src = URL(fileURLWithPath: a[1]), dst = URL(fileURLWithPath: a[2])
let outW = Int(a[3])!, bitrate = Int(a[4])!
try? FileManager.default.removeItem(at: dst)
let asset = AVURLAsset(url: src)
let track = asset.tracks(withMediaType: .video)[0]
precondition(track.preferredTransform.isIdentity, "rotated source not handled")
let n = track.naturalSize
var outH = Int((Double(outW) * Double(n.height) / Double(n.width)).rounded()); outH += outH % 2
let reader = try AVAssetReader(asset: asset)
let rOut = AVAssetReaderTrackOutput(track: track, outputSettings: [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange])
reader.add(rOut)
let writer = try AVAssetWriter(outputURL: dst, fileType: .mp4)
writer.shouldOptimizeForNetworkUse = true
let wIn = AVAssetWriterInput(mediaType: .video, outputSettings: [
  AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: outW, AVVideoHeightKey: outH,
  AVVideoScalingModeKey: AVVideoScalingModeResizeAspectFill,
  AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: bitrate, AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
                                    AVVideoMaxKeyFrameIntervalDurationKey: 2, AVVideoH264EntropyModeKey: AVVideoH264EntropyModeCABAC]])
wIn.expectsMediaDataInRealTime = false
writer.add(wIn)
reader.startReading(); writer.startWriting()
var started = false
let q = DispatchQueue(label: "enc"), done = DispatchSemaphore(value: 0)
wIn.requestMediaDataWhenReady(on: q) {
  while wIn.isReadyForMoreMediaData {
    guard let sb = rOut.copyNextSampleBuffer() else { wIn.markAsFinished(); writer.finishWriting { done.signal() }; return }
    if !started { writer.startSession(atSourceTime: CMSampleBufferGetPresentationTimeStamp(sb)); started = true }
    wIn.append(sb)
  }
}
done.wait()
print(writer.status == .completed ? "ok \(outW)x\(outH) fps=\(track.nominalFrameRate)" : "failed: \(String(describing: writer.error))")
