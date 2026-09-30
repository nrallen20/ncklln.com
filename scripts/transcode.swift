// transcode <src> <dst.mp4> <width> <bitrate-bps> [crop-top-px] [keep-every-nth-frame]: H.264, no audio, faststart.
// crop-top removes that many source pixels from the top (e.g. a screen recording's browser chrome);
// keep-every-nth-frame = 2 turns a 60 fps recording into 30 fps, which UI footage never misses.
import AVFoundation
let a = CommandLine.arguments
let src = URL(fileURLWithPath: a[1]), dst = URL(fileURLWithPath: a[2])
let outW = Int(a[3])!, bitrate = Int(a[4])!, cropTop = a.count > 5 ? Int(a[5])! : 0, keepEvery = a.count > 6 ? Int(a[6])! : 1
try? FileManager.default.removeItem(at: dst)
let asset = AVURLAsset(url: src)
let track = asset.tracks(withMediaType: .video)[0]
precondition(track.preferredTransform.isIdentity, "rotated source not handled")
let n = track.naturalSize
let srcH = Int(n.height) - cropTop
var outH = Int((Double(outW) * Double(srcH) / Double(n.width)).rounded()); outH += outH % 2
let reader = try AVAssetReader(asset: asset)
let pixelFormat = [kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange]
let rOut: AVAssetReaderOutput
if cropTop > 0 {
  let comp = AVMutableVideoComposition()
  comp.renderSize = CGSize(width: n.width, height: CGFloat(srcH))
  comp.frameDuration = CMTime(value: 1, timescale: CMTimeScale(track.nominalFrameRate.rounded()))
  let inst = AVMutableVideoCompositionInstruction()
  inst.timeRange = CMTimeRange(start: .zero, duration: asset.duration)
  let layer = AVMutableVideoCompositionLayerInstruction(assetTrack: track)
  layer.setTransform(CGAffineTransform(translationX: 0, y: CGFloat(-cropTop)), at: .zero)
  inst.layerInstructions = [layer]
  comp.instructions = [inst]
  let o = AVAssetReaderVideoCompositionOutput(videoTracks: [track], videoSettings: pixelFormat)
  o.videoComposition = comp
  rOut = o
} else {
  rOut = AVAssetReaderTrackOutput(track: track, outputSettings: pixelFormat)
}
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
var started = false, frameIndex = 0
let q = DispatchQueue(label: "enc"), done = DispatchSemaphore(value: 0)
wIn.requestMediaDataWhenReady(on: q) {
  while wIn.isReadyForMoreMediaData {
    guard let sb = rOut.copyNextSampleBuffer() else { wIn.markAsFinished(); writer.finishWriting { done.signal() }; return }
    if !started { writer.startSession(atSourceTime: CMSampleBufferGetPresentationTimeStamp(sb)); started = true }
    if frameIndex % keepEvery == 0 { wIn.append(sb) }
    frameIndex += 1
  }
}
done.wait()
print(writer.status == .completed ? "ok \(outW)x\(outH) fps=\(track.nominalFrameRate)" : "failed: \(String(describing: writer.error))")
